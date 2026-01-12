from datetime import timedelta

import pytest
from django.core import mail
from django.utils import timezone

from sloth.attendance.models import Attendance
from sloth.attendance.models import Practice
from sloth.attendance.models import Skater
from sloth.attendance.tasks import send_unpaid_attendance_reminders


@pytest.mark.django_db
class TestAttendanceTasks:
    def test_send_unpaid_attendance_reminders(self):
        # Create a skater with guardian email
        skater = Skater.objects.create(
            name="Test Skater",
            jersey_number="12",
            guardian_email="guardian@example.com",
        )

        # Create a practice 5 days ago
        five_days_ago = timezone.now().date() - timedelta(days=5)
        practice = Practice.objects.create(date=five_days_ago, location="The Rink")

        # Create an unpaid attendance record
        attendance = Attendance.objects.create(
            skater=skater,
            practice=practice,
            paid=False,
            status=Attendance.Status.PRESENT,
        )

        # Create an attendance record from today (should NOT be picked up)
        today_practice = Practice.objects.create(
            date=timezone.now().date(),
            location="The Rink",
        )
        Attendance.objects.create(
            skater=skater,
            practice=today_practice,
            paid=False,
            status=Attendance.Status.PRESENT,
        )

        # Create an unpaid record from 5 days ago BUT reminder already sent
        skater_sent = Skater.objects.create(
            name="Sent Skater",
            jersey_number="13",
            guardian_email="sent@example.com",
        )
        Attendance.objects.create(
            skater=skater_sent,
            practice=practice,
            paid=False,
            reminder_sent=True,
            status=Attendance.Status.PRESENT,
        )

        # Create a PAID record from 5 days ago (should NOT be picked up)
        skater_paid = Skater.objects.create(
            name="Paid Skater",
            jersey_number="14",
            guardian_email="paid@example.com",
        )
        Attendance.objects.create(
            skater=skater_paid,
            practice=practice,
            paid=True,
            status=Attendance.Status.PRESENT,
        )

        # Run the task
        send_unpaid_attendance_reminders.call_local()

        # Check that only one email was sent
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.to == ["guardian@example.com"]
        assert "Attendance Payment Reminder" in email.subject
        assert skater.name in email.body
        assert str(practice.date) in email.body

        # Check that reminder_sent was updated
        attendance.refresh_from_db()
        assert attendance.reminder_sent is True

    def test_send_unpaid_attendance_reminders_custom_days(self, settings):
        # Override setting to 3 days
        settings.UNPAID_ATTENDANCE_REMINDER_DAYS = 3

        skater = Skater.objects.create(
            name="Custom Skater",
            jersey_number="15",
            guardian_email="custom@example.com",
        )

        # Create a practice 3 days ago
        three_days_ago = timezone.now().date() - timedelta(days=3)
        practice = Practice.objects.create(date=three_days_ago, location="The Rink")

        Attendance.objects.create(
            skater=skater,
            practice=practice,
            paid=False,
            status=Attendance.Status.PRESENT,
        )

        # Run the task
        send_unpaid_attendance_reminders.call_local()

        # Check that email was sent
        assert any(email.to == ["custom@example.com"] for email in mail.outbox)

    def test_send_unpaid_attendance_reminders_no_guardian_email(self):
        """Test that skaters without guardian emails are correctly filtered out."""
        # Create a practice 5 days ago
        five_days_ago = timezone.now().date() - timedelta(days=5)
        practice = Practice.objects.create(date=five_days_ago, location="The Rink")

        # Create a skater with None guardian email (blank=True in model)
        skater_no_email = Skater.objects.create(
            name="No Email Skater",
            jersey_number="20",
            guardian_email="",  # Empty string
        )

        # Create unpaid attendance for skater without email
        Attendance.objects.create(
            skater=skater_no_email,
            practice=practice,
            paid=False,
            status=Attendance.Status.PRESENT,
        )

        # Create another skater with a valid email for comparison
        skater_with_email = Skater.objects.create(
            name="Valid Email Skater",
            jersey_number="21",
            guardian_email="valid@example.com",
        )

        # Create unpaid attendance for skater with email
        Attendance.objects.create(
            skater=skater_with_email,
            practice=practice,
            paid=False,
            status=Attendance.Status.PRESENT,
        )

        # Run the task
        send_unpaid_attendance_reminders.call_local()

        # Check that only one email was sent (to the skater with valid email)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["valid@example.com"]

        # Verify the skater without email did not get a reminder sent flag
        attendance_no_email = Attendance.objects.get(skater=skater_no_email)
        assert attendance_no_email.reminder_sent is False

        # Verify the skater with email got the reminder sent flag
        attendance_with_email = Attendance.objects.get(skater=skater_with_email)
        assert attendance_with_email.reminder_sent is True
