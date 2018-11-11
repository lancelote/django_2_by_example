import pytest
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
