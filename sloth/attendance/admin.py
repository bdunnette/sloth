from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Attendance
from .models import Practice
from .models import Skater


@admin.register(Skater)
class SkaterAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ["name", "jersey_number", "tag_list", "guardian_email"]
    list_filter = ["tags"]
    search_fields = ["name", "legal_name", "jersey_number"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


@admin.register(Practice)
class PracticeAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ["date", "location", "is_canceled"]
    list_filter = ["is_canceled", "date"]
    search_fields = ["location"]


@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ["skater", "practice", "status", "paid"]
    list_filter = ["status", "paid", "practice", "skater"]
    search_fields = ["skater__name", "practice__location"]
