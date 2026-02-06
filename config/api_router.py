from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from sloth.skaters.api.views import AttendanceViewSet
from sloth.skaters.api.views import CoachViewSet
from sloth.skaters.api.views import GuardianViewSet
from sloth.skaters.api.views import SkaterViewSet
from sloth.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("skaters", SkaterViewSet)
router.register("coaches", CoachViewSet)
router.register("guardians", GuardianViewSet)
router.register("attendance", AttendanceViewSet)


app_name = "api"
urlpatterns = router.urls
