from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import periodic_task

from .models import Attendance


@periodic_task(crontab(hour=8, minute=0))  # Daily at 8:00 AM
def send_unpaid_attendance_reminders():
    """
    Sends email reminders to guardians for attendance records that remain unpaid
    after a configurable number of days
    (defined by UNPAID_ATTENDANCE_REMINDER_DAYS setting).
    """
    five_days_ago = timezone.now().date() - timedelta(
        days=settings.UNPAID_ATTENDANCE_REMINDER_DAYS,
    )

    unpaid_attendance = (
        Attendance.objects.filter(
            practice__date=five_days_ago,
            paid=False,
            reminder_sent=False,
            status=Attendance.Status.PRESENT,
            skater__guardian_email__isnull=False,
        )
        .exclude(skater__guardian_email="")
        .select_related("skater", "practice")
    )

    records_to_update = []
    for attendance in unpaid_attendance:
        skater = attendance.skater
        practice = attendance.practice

        subject = f"Attendance Payment Reminder: {skater.name} - {practice.date}"
        message = (
            f"Hi,\n\n"
            f"This is a reminder that the practice attendance for {skater.name} on "
            f"{practice.date} at {practice.location} is currently marked as unpaid.\n\n"
            f"Please ensure payment is made at your earliest convenience.\n\n"
            f"Thank you!\n"
            f"Sloth Derby Team"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[skater.guardian_email],
            fail_silently=False,
        )

        attendance.reminder_sent = True
        records_to_update.append(attendance)

    # Bulk update all reminder_sent flags in a single database query
    if records_to_update:
        Attendance.objects.bulk_update(records_to_update, ["reminder_sent"])
