from huey.contrib.djhuey import task

from .models import User


@task()
def get_users_count():
    """A pointless Huey task to demonstrate usage."""
    return User.objects.count()
