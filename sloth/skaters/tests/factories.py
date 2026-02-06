from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from sloth.skaters.models import Attendance
from sloth.skaters.models import Coach
from sloth.skaters.models import Guardian
from sloth.skaters.models import Skater


class GuardianFactory(DjangoModelFactory[Guardian]):
    name = Faker("name")
    email = Faker("email")
    phone = Faker("phone_number")

    class Meta:
        model = Guardian


class CoachFactory(DjangoModelFactory[Coach]):
    name = Faker("name")
    derby_name = Faker("first_name")
    derby_number = Faker("numerify", text="##")
    email = Faker("email")
    phone = Faker("phone_number")
    is_active = True

    class Meta:
        model = Coach


class SkaterFactory(DjangoModelFactory[Skater]):
    name = Faker("name")
    derby_name = Faker("first_name")
    derby_number = Faker("numerify", text="##")
    email = Faker("email")
    phone = Faker("phone_number")
    date_of_birth = Faker("date_of_birth", minimum_age=5, maximum_age=18)
    is_active = True

    class Meta:
        model = Skater


class AttendanceFactory(DjangoModelFactory[Attendance]):
    skater = SubFactory(SkaterFactory)
    date = Faker("date_this_year")
    paid_dues = False
    notes = Faker("sentence")

    class Meta:
        model = Attendance
