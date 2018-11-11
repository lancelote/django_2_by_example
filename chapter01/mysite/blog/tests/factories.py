import factory
from django.contrib.auth.models import User
from factory import Faker as Fake


class UserFactory(factory.django.DjangoModelFactory):
    username = Fake('user_name')
    first_name = Fake('first_name')
    last_name = Fake('last_name')
    email = Fake('email')
    is_staff = False

    class Meta:
        model = User


class PostFactory(factory.django.DjangoModelFactory):
    title = Fake('sentence', nb_words=4)
    slug = Fake('slug')
    author = factory.SubFactory(UserFactory)
    body = Fake('text', max_nb_chars=200)

    class Meta:
        model = 'blog.Post'
