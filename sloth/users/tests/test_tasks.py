import pytest

from sloth.users.tasks import get_users_count
from sloth.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    """A basic test to execute the get_users_count Huey task."""
    batch_size = 3
    UserFactory.create_batch(batch_size)
    # Force immediate execution
    settings.HUEY["immediate"] = True

    # In immediate mode with django-huey, the task is executed
    # and returns the result directly (or a wrapper depending on version,
    # but usually behaves like normal function call if immediate=True)
    # However, django-huey might still return a result object or the value.
    # Let's assume it returns the value or we check result()

    # Run the task function directly, bypassing the queue
    result = get_users_count.call_local()
    assert result == batch_size
