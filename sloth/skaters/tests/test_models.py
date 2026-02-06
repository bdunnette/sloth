from datetime import date

from django.test import TestCase
from django.utils import timezone

from .factories import AttendanceFactory
from .factories import CoachFactory
from .factories import GuardianFactory
from .factories import SkaterFactory


class SkaterModelTest(TestCase):
    def setUp(self):
        self.guardian1 = GuardianFactory(name="Jane Doe")
        self.guardian2 = GuardianFactory(name="John Doe")
        self.skater = SkaterFactory(
            name="Kid Doe",
            date_of_birth=date(2015, 1, 1),
        )
        self.skater.guardians.add(self.guardian1, self.guardian2)

    def test_skater_creation(self):
        expected_guardian_count = 2
        assert self.skater.name == "Kid Doe"
        assert self.skater.date_of_birth == date(2015, 1, 1)
        assert self.skater.guardians.count() == expected_guardian_count
        assert self.guardian1 in self.skater.guardians.all()
        assert self.guardian2 in self.skater.guardians.all()

    def test_str_methods(self):
        assert str(self.guardian1) == "Jane Doe"
        assert str(self.skater) == f"{self.skater.derby_name} (Kid Doe)"


class CoachModelTest(TestCase):
    def test_coach_creation(self):
        coach = CoachFactory(name="Coach Name", derby_name="The Coach")
        assert coach.name == "Coach Name"
        assert coach.derby_name == "The Coach"
        assert str(coach) == "The Coach (Coach Name)"


class AttendanceModelTest(TestCase):
    def setUp(self):
        self.skater = SkaterFactory(name="Kid Doe", derby_name="")
        self.today = timezone.now().date()
        self.attendance = AttendanceFactory(skater=self.skater, date=self.today)

    def test_attendance_creation(self):
        assert self.attendance.skater == self.skater
        assert self.attendance.date == self.today

    def test_str_method(self):
        expected_str = f"Kid Doe - {self.today}"
        assert str(self.attendance) == expected_str
