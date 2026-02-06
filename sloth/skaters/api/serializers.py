from rest_framework import serializers

from sloth.skaters.models import Attendance
from sloth.skaters.models import Coach
from sloth.skaters.models import Guardian
from sloth.skaters.models import Skater


class GuardianSerializer(serializers.ModelSerializer[Guardian]):
    class Meta:
        model = Guardian
        fields = ["id", "name", "email", "phone"]


class CoachSerializer(serializers.ModelSerializer[Coach]):
    class Meta:
        model = Coach
        fields = [
            "id",
            "name",
            "derby_name",
            "derby_number",
            "email",
            "phone",
            "is_active",
        ]


class SkaterSerializer(serializers.ModelSerializer[Skater]):
    guardians = GuardianSerializer(many=True, read_only=True)
    guardian_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Guardian.objects.all(),
        source="guardians",
        write_only=True,
    )

    class Meta:
        model = Skater
        fields = [
            "id",
            "name",
            "derby_name",
            "derby_number",
            "email",
            "phone",
            "date_of_birth",
            "guardians",
            "guardian_ids",
            "is_active",
        ]


class AttendanceSerializer(serializers.ModelSerializer[Attendance]):
    person_name = serializers.SerializerMethodField()
    derby_name = serializers.SerializerMethodField()
    person_type = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "skater",
            "coach",
            "person_name",
            "derby_name",
            "person_type",
            "date",
            "paid_dues",
            "notes",
        ]

    def get_person_name(self, obj):
        if obj.skater:
            return obj.skater.name
        if obj.coach:
            return obj.coach.name
        return "Unknown"

    def get_derby_name(self, obj):
        if obj.skater:
            return obj.skater.derby_name
        if obj.coach:
            return obj.coach.derby_name
        return ""

    def get_person_type(self, obj):
        if obj.skater:
            return "skater"
        if obj.coach:
            return "coach"
        return "unknown"
