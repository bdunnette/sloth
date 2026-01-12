import pytest
from django.utils import timezone

from sloth.attendance.models import Attendance
from sloth.attendance.models import Practice
from sloth.attendance.models import Skater


@pytest.mark.django_db
class TestAttendance:
    def test_record_attendance(self):
        skater = Skater.objects.create(name="Roller Girl", jersey_number="55")
        practice = Practice.objects.create(
            date=timezone.now().date(),
            location="The Rink",
        )

        attendance = Attendance.objects.create(
            skater=skater,
            practice=practice,
            status=Attendance.Status.PRESENT,
            paid=False,
        )

        assert attendance.status == Attendance.Status.PRESENT
        assert not attendance.paid

    def test_mark_paid(self):
        skater = Skater.objects.create(name="Roller Guy", jersey_number="88")
        practice = Practice.objects.create(
            date=timezone.now().date(),
            location="The Rink",
        )
        attendance = Attendance.objects.create(skater=skater, practice=practice)

        attendance.paid = True
        attendance.save()

    def test_signin_view(self, client):
        skater = Skater.objects.create(name="Signin Skater", jersey_number="99")
        skater.tags.add("Active")
        practice = Practice.objects.create(
            date=timezone.now().date(),
            location="The Rink",
        )
        url = "/attendance/signin/"

        # Test GET
        get_success_code = 200
        response = client.get(url)
        assert response.status_code == get_success_code

        # Test POST
        post_success_code = 302
        response = client.post(url, {"skater": skater.pk})
        assert response.status_code == post_success_code

        # Verify attendance created
        assert Attendance.objects.filter(
            skater=skater,
            practice=practice,
            status=Attendance.Status.PRESENT,
        ).exists()
