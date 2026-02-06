from django.contrib import admin

from .models import Attendance
from .models import Coach
from .models import Guardian
from .models import Skater


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email")


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ("name", "derby_name", "derby_number", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "derby_name", "derby_number")


@admin.register(Skater)
class SkaterAdmin(admin.ModelAdmin):
    list_display = ("name", "derby_name", "derby_number", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "derby_name", "derby_number")
    filter_horizontal = ("guardians",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("get_person_name", "date", "paid_dues")
    list_filter = ("date", "paid_dues")
    date_hierarchy = "date"

    @admin.display(
        description="Person",
    )
    def get_person_name(self, obj):
        return (
            obj.skater.name
            if obj.skater
            else (obj.coach.name if obj.coach else "Unknown")
        )
