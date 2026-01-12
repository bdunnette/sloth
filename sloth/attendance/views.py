from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import SigninForm
from .models import Attendance
from .models import Practice
from .models import Skater


class SkaterListView(LoginRequiredMixin, ListView):
    model = Skater
    template_name = "attendance/skater_list.html"
    context_object_name = "skaters"

    def get_queryset(self):
        return Skater.objects.prefetch_related("tags").all()


class SkaterCreateView(LoginRequiredMixin, CreateView):
    model = Skater
    template_name = "attendance/skater_form.html"
    fields = [
        "name",
        "legal_name",
        "jersey_number",
        "tags",
        "photo",
        "guardian_email",
    ]
    success_url = reverse_lazy("attendance:skater_list")


class SkaterUpdateView(LoginRequiredMixin, UpdateView):
    model = Skater
    template_name = "attendance/skater_form.html"
    fields = [
        "name",
        "legal_name",
        "jersey_number",
        "tags",
        "photo",
        "guardian_email",
    ]
    success_url = reverse_lazy("attendance:skater_list")


class SkaterDeleteView(LoginRequiredMixin, DeleteView):
    model = Skater
    template_name = "attendance/skater_confirm_delete.html"
    success_url = reverse_lazy("attendance:skater_list")


class PracticeListView(LoginRequiredMixin, ListView):
    model = Practice
    template_name = "attendance/practice_list.html"
    context_object_name = "practices"
    ordering = ["-date"]


class PracticeCreateView(LoginRequiredMixin, CreateView):
    model = Practice
    template_name = "attendance/practice_form.html"
    fields = ["date", "location", "is_canceled"]
    success_url = reverse_lazy("attendance:practice_list")


class PracticeUpdateView(LoginRequiredMixin, UpdateView):
    model = Practice
    template_name = "attendance/practice_form.html"
    fields = ["date", "location", "is_canceled"]
    success_url = reverse_lazy("attendance:practice_list")


class PracticeDeleteView(LoginRequiredMixin, DeleteView):
    model = Practice
    template_name = "attendance/practice_confirm_delete.html"
    success_url = reverse_lazy("attendance:practice_list")


class PracticeDetailView(LoginRequiredMixin, ListView):
    """
    Shows the attendance list for a specific practice.
    Using ListView to list Attendance records, but with extra context for the Practice.
    """

    model = Attendance
    template_name = "attendance/practice_detail.html"
    context_object_name = "attendance_records"

    def get_queryset(self):
        return Attendance.objects.filter(practice_id=self.kwargs["pk"]).select_related(
            "skater",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["practice"] = Practice.objects.get(pk=self.kwargs["pk"])
        return context


class PracticeAttendanceUpdateView(LoginRequiredMixin, FormView):
    template_name = "attendance/attendance_form.html"

    def get_success_url(self):
        return reverse("attendance:practice_detail", kwargs={"pk": self.kwargs["pk"]})

    def get_form(self, form_class=None):
        practice = get_object_or_404(Practice, pk=self.kwargs["pk"])
        # Ensure attendance records exist for all active skaters
        active_skaters = Skater.objects.filter(tags__name__in=["Active"])
        for skater in active_skaters:
            Attendance.objects.get_or_create(practice=practice, skater=skater)

        attendance_form_set = modelformset_factory(
            Attendance,
            fields=("status", "paid", "notes"),
            extra=0,
            can_delete=False,
        )
        return attendance_form_set(
            self.request.POST or None,
            queryset=Attendance.objects.filter(practice=practice).select_related(
                "skater",
            ),
        )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["practice"] = get_object_or_404(Practice, pk=self.kwargs["pk"])
        return context


class TodaysAttendanceView(ListView):
    model = Attendance
    template_name = "attendance/public_list.html"
    context_object_name = "attendance_records"

    def get_queryset(self):
        return (
            Attendance.objects.filter(
                practice__date=timezone.now().date(),
                status=Attendance.Status.PRESENT,
            )
            .exclude(skater__tags__name__in=["Coach"])
            .select_related("skater")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now().date()
        context["coaches"] = Skater.objects.filter(tags__name__in=["Coach"]).order_by(
            "name",
        )
        return context


class SigninView(FormView):
    template_name = "attendance/signin.html"
    form_class = SigninForm
    success_url = reverse_lazy("attendance:signin")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if there is a practice for today
        today = timezone.now().date()
        practice = Practice.objects.filter(date=today, is_canceled=False).first()
        context["practice"] = practice

        # Add recently signed in skater if in session/messages
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        today = timezone.now().date()
        practice = Practice.objects.filter(date=today, is_canceled=False).first()

        if practice:
            signed_in_skaters = Attendance.objects.filter(
                practice=practice,
                status=Attendance.Status.PRESENT,
            ).values_list("skater_id", flat=True)
            form.fields["skater"].queryset = (
                form.fields["skater"]
                .queryset.exclude(id__in=signed_in_skaters)
                .order_by("name")
            )
        return form

    def form_valid(self, form):
        today = timezone.now().date()
        practice = Practice.objects.filter(date=today, is_canceled=False).first()

        if not practice:
            messages.error(self.request, "No practice scheduled for today.")
            return self.form_invalid(form)

        skater = form.cleaned_data["skater"]

        # Create or update attendance record
        attendance, created = Attendance.objects.get_or_create(
            practice=practice,
            skater=skater,
            defaults={"status": Attendance.Status.PRESENT},
        )

        if not created and attendance.status != Attendance.Status.PRESENT:
            attendance.status = Attendance.Status.PRESENT
            attendance.save()

        messages.success(self.request, f"Welcome, {skater.name}! You are signed in.")
        return super().form_valid(form)
