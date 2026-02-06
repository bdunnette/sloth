from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from sloth.skaters.models import Attendance
from sloth.skaters.models import Coach
from sloth.skaters.models import Guardian
from sloth.skaters.models import Skater

from .serializers import AttendanceSerializer
from .serializers import CoachSerializer
from .serializers import GuardianSerializer
from .serializers import SkaterSerializer


class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        active_only = self.request.query_params.get("active", None)
        if active_only is not None:
            queryset = queryset.filter(is_active=True)
        return queryset


class SkaterViewSet(viewsets.ModelViewSet):
    queryset = Skater.objects.all()
    serializer_class = SkaterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        active_only = self.request.query_params.get("active", None)
        if active_only is not None:
            queryset = queryset.filter(is_active=True)
        return queryset


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by today by default if no date specified?
        # Or just let the frontend handle filtering.
        # Let's add simple filters.
        skater_id = self.request.query_params.get("skater", None)
        if skater_id is not None:
            queryset = queryset.filter(skater_id=skater_id)

        coach_id = self.request.query_params.get("coach", None)
        if coach_id is not None:
            queryset = queryset.filter(coach_id=coach_id)

        today_only = self.request.query_params.get("today", None)
        if today_only is not None:
            queryset = queryset.filter(date=now().date())

        return queryset
