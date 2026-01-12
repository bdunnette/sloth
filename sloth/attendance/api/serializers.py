from rest_framework import serializers

from sloth.attendance.models import Attendance
from sloth.attendance.models import Practice
from sloth.attendance.models import Skater


class SkaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skater
        fields = [
            "id",
            "name",
            "legal_name",
            "jersey_number",
            "is_active",
            "guardian_email",
        ]


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = ["id", "date", "location", "is_canceled"]


class AttendanceSerializer(serializers.ModelSerializer):
    skater_name = serializers.CharField(source="skater.name", read_only=True)
    practice_display = serializers.CharField(source="practice.__str__", read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id",
            "skater",
            "skater_name",
            "practice",
            "practice_display",
            "status",
            "paid",
            "notes",
        ]
