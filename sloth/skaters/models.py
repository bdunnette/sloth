from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    """Abstract base model for all individuals."""

    name = models.CharField(_("Legal Name"), max_length=255)
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DerbyPerson(Person):
    """Abstract base for skaters and coaches with derby identities."""

    derby_name = models.CharField(_("Derby Name"), max_length=255, blank=True)
    derby_number = models.CharField(_("Derby Number"), max_length=10, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.derby_name:
            return f"{self.derby_name} ({self.name})"
        return self.name


class Guardian(Person):
    """Adult guardian contact information."""


class Skater(DerbyPerson):
    """Junior roller derby skater."""

    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    guardians = models.ManyToManyField(
        Guardian,
        related_name="skaters",
        verbose_name=_("Guardians"),
        blank=True,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)


class Coach(DerbyPerson):
    """Roller derby coach."""

    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name_plural = _("Coaches")


class Attendance(models.Model):
    """Tracking attendance for skaters and coaches."""

    skater = models.ForeignKey(
        Skater,
        on_delete=models.CASCADE,
        related_name="attendances",
        null=True,
        blank=True,
    )
    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        related_name="attendances",
        null=True,
        blank=True,
    )
    date = models.DateField(_("Date"), auto_now_add=True)
    paid_dues = models.BooleanField(_("Paid Dues"), default=False)
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def __str__(self):
        person_name = "Unknown"
        if self.skater:
            person_name = self.skater.derby_name or self.skater.name
        elif self.coach:
            person_name = self.coach.derby_name or self.coach.name
        return f"{person_name} - {self.date}"
