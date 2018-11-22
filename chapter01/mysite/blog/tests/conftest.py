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
    """Custom wrapper around the selenium fixture."""

    def login(username, password):
        """Login given user into django admin

        Args:
            username (str)
            password (str)
        """
        login_form = selenium.find_element_by_id('login-form')
        login_form.find_element_by_name('username').send_keys(username)
        login_form.find_element_by_name('password').send_keys(password)
        login_form.find_element_by_css_selector('.submit-row input').click()

    def search_model_by(text):
        """Search a model in admin panel by the given text."""
        search_field = selenium.find_element_by_id('searchbar')
        search_button = selenium.find_element_by_css_selector('#changelist-search input[type="submit"]')

        search_field.clear()
        search_field.send_keys(text)
        search_button.click()

        return selenium.find_elements_by_css_selector('#result_list [class^="row"]')

    assert not hasattr(selenium, 'login')
    selenium.login = login

    assert not hasattr(selenium, 'search_model_by')
    selenium.search_model_by = search_model_by

    return selenium
