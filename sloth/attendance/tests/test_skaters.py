import pytest

from sloth.attendance.models import Skater


@pytest.mark.django_db
class TestSkater:
    def test_create_skater(self):
        skater = Skater.objects.create(
            name="Sloth Racer",
            jersey_number="123",
            legal_name="Sid Sloth",
            guardian_email="mom@sloth.com",
        )
        assert skater.name == "Sloth Racer"
        assert skater.pk is not None

    def test_update_skater(self):
        skater = Skater.objects.create(name="Sloth Racer", jersey_number="123")
        skater.name = "Fast Sloth"
        skater.save()

        updated_skater = Skater.objects.get(pk=skater.pk)
        assert updated_skater.name == "Fast Sloth"
