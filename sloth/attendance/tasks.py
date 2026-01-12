import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import periodic_task

from .models import Attendance

logger = logging.getLogger(__name__)


@periodic_task(crontab(hour=8, minute=0))  # Daily at 8:00 AM
def send_unpaid_attendance_reminders():
    """
    Sends email reminders to guardians for attendance records that remain unpaid
    after 5 days.
    """
    five_days_ago = timezone.now().date() - timedelta(
        days=settings.UNPAID_ATTENDANCE_REMINDER_DAYS,
    )

    unpaid_attendance = (
        Attendance.objects.filter(
            practice__date=five_days_ago,
            paid=False,
            reminder_sent=False,
            skater__guardian_email__isnull=False,
        )
        .exclude(skater__guardian_email="")
        .select_related("skater", "practice")
    )

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

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[skater.guardian_email],
                fail_silently=False,
            )
            attendance.reminder_sent = True
            attendance.save()
        except Exception as e:
            logger.error(
                f"Failed to send reminder email for attendance {attendance.id} "
                f"(skater: {skater.name}, practice: {practice.date}): {e}",
            )
