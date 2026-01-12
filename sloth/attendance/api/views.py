from rest_framework import viewsets

from sloth.attendance.models import Attendance
from sloth.attendance.models import Skater

from .serializers import AttendanceSerializer
from .serializers import SkaterSerializer


class SkaterViewSet(viewsets.ModelViewSet):
    queryset = Skater.objects.all()
    serializer_class = SkaterSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filterset_fields = ["skater", "practice", "status", "paid"]
