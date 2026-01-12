from django.urls import path

from .views import PracticeAttendanceUpdateView
from .views import PracticeCreateView
from .views import PracticeDeleteView
from .views import PracticeDetailView
from .views import PracticeListView
from .views import PracticeUpdateView
from .views import SigninView
from .views import SkaterCreateView
from .views import SkaterDeleteView
from .views import SkaterListView
from .views import SkaterUpdateView

app_name = "attendance"
urlpatterns = [
    path("skaters/", SkaterListView.as_view(), name="skater_list"),
    path("skaters/add/", SkaterCreateView.as_view(), name="skater_add"),
    path("skaters/<int:pk>/", SkaterUpdateView.as_view(), name="skater_edit"),
    path("skaters/<int:pk>/delete/", SkaterDeleteView.as_view(), name="skater_delete"),
    path("practices/", PracticeListView.as_view(), name="practice_list"),
    path("practices/add/", PracticeCreateView.as_view(), name="practice_add"),
    path("practices/<int:pk>/", PracticeDetailView.as_view(), name="practice_detail"),
    path(
        "practices/<int:pk>/edit/",
        PracticeUpdateView.as_view(),
        name="practice_edit",
    ),
    path(
        "practices/<int:pk>/attendance/",
        PracticeAttendanceUpdateView.as_view(),
        name="practice_attendance_edit",
    ),
    path(
        "practices/<int:pk>/delete/",
        PracticeDeleteView.as_view(),
        name="practice_delete",
    ),
    path("signin/", SigninView.as_view(), name="signin"),
]
