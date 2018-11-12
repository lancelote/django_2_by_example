import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from pytest_factoryboy import register

from blog.tests.factories import PostFactory, UserFactory

register(UserFactory)
register(PostFactory)


@pytest.fixture
def mock_now(mocker):
    new_now = timezone.now()
    with mocker.patch('django.utils.timezone.now', return_value=new_now):
        yield new_now


@pytest.fixture
def admin():
    return get_user_model().objects.create_superuser(username='admin', email='admin@example.com', password='password')


@pytest.fixture
def browser(selenium):
    """Readable wrapper around selenium fixture."""
    return selenium
