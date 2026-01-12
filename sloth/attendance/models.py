from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager


class Skater(models.Model):
    name = models.CharField(_("Derby Name"), max_length=255)
    legal_name = models.CharField(_("Legal Name"), max_length=255, blank=True)
    jersey_number = models.CharField(_("Jersey Number"), max_length=50)
    photo = models.ImageField(_("Photo"), upload_to="skaters/", blank=True)
    guardian_email = models.EmailField(_("Guardian Email"), blank=True)

    tags = TaggableManager()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} #{self.jersey_number}"

    def is_active(self):
        return self.tags.filter(name="Active").exists()

    def is_coach(self):
        return self.tags.filter(name="Coach").exists()


class Practice(models.Model):
    date = models.DateField(_("Date"))
    location = models.CharField(_("Location"), max_length=255)
    is_canceled = models.BooleanField(_("Canceled"), default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.date} @ {self.location}"


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", _("Present")
        ABSENT = "ABSENT", _("Absent")
        EXCUSED = "EXCUSED", _("Excused")

    skater = models.ForeignKey(
        Skater,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    practice = models.ForeignKey(
        Practice,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=Status.choices,
        default=Status.PRESENT,
    )
    paid = models.BooleanField(_("Paid"), default=False)
    notes = models.TextField(_("Notes"), blank=True)
    reminder_sent = models.BooleanField(_("Reminder Sent"), default=False)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("skater", "practice")

    def __str__(self):
        return f"{self.skater} @ {self.practice}: {self.status}"
