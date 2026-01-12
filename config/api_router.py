from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from sloth.attendance.api.views import AttendanceViewSet
from sloth.attendance.api.views import SkaterViewSet
from sloth.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("skaters", SkaterViewSet)
router.register("attendance", AttendanceViewSet)


app_name = "api"
urlpatterns = router.urls
