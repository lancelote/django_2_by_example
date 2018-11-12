from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from blog.models import Post, User

pytestmark = pytest.mark.django_db


class TestPost:

    def test_slug_must_be_unique(self, post_factory):
        post1 = post_factory(slug='foo')
        with pytest.raises(ValidationError, match='Slug must be unique for Publish date.'):
            # Not a database constraint, should validate manually
            post2 = post_factory(slug='foo', publish=post1.publish)
            post2.validate_unique()

    def test_same_slug_for_different_dates(self, post_factory):
        post1 = post_factory(slug='foo')
        try:
            post2 = post_factory(slug='foo', publish=post1.publish + timedelta(days=1))
            post2.validate_unique()
        except ValidationError:
            pytest.fail('Slug may be the same for the different Publish dates.')

    def test_slug_should_not_exceed_250_chars(self, post_factory):
        post_factory(slug='a' * 250).clean_fields()
        with pytest.raises(ValidationError, match='Ensure this value has at most 250 characters'):
            post_factory(slug='a' * 251).clean_fields()

    def test_title_should_not_exceed_250_chars(self, post_factory):
        post_factory(title='a' * 250).clean_fields()
        with pytest.raises(ValidationError, match='Ensure this value has at most 250 characters'):
            post_factory(title='a' * 251).clean_fields()

    def test_get_user_posts(self, post_factory, user_factory):
        user1 = user_factory()
        user2 = user_factory()
        post1 = post_factory(author=user1)
        post2 = post_factory(author=user2)
        post3 = post_factory(author=user1)

        user1_posts = user1.blog_posts.all()
        user2_posts = user2.blog_posts.all()

        assert list(user1_posts) == [post3, post1]
        assert list(user2_posts) == [post2]

    def test_remove_user_remove_blog_posts(self, post_factory, user_factory):
        user1 = user_factory()
        user2 = user_factory()
        post_factory(author=user1)
        post2 = post_factory(author=user2)
        post_factory(author=user1)

        user1.delete()

        assert list(Post.objects.all()) == [post2]
        assert list(User.objects.all()) == [user2]

    def test_default_publish_date_is_now(self, post_factory, mock_now):
        assert post_factory().publish == mock_now

    def test_created_is_set_on_creation_moment(self, post_factory, mock_now):
        assert post_factory().created == mock_now

    def test_updated_is_set_on_update(self, post_factory, mocker):
        post = post_factory()
        new_now = timezone.now()
        with mocker.patch('django.utils.timezone.now', return_value=new_now):
            post.title = 'foo'
            post.save()
            assert post.updated == new_now

    def test_default_status_is_draft(self, post_factory):
        assert post_factory().status == 'draft'

    def test_published_status_is_ok(self, post_factory):
        try:
            post_factory(status='published').clean_fields()
        except ValidationError:
            pytest.fail('"published" should be a possible choice for a post status.')

    def test_unknown_status_is_not_ok(self, post_factory):
        with pytest.raises(ValidationError, match='is not a valid choice'):
            post_factory(status='unknown').clean_fields()

    def test_max_status_length(self):
        assert all(len(status) <= 10 for (status, Status) in Post.STATUS_CHOICES)

    def test_post_order_reverse_by_publish(self, post_factory):
        posts = [post_factory() for _ in range(3)]
        assert list(Post.objects.all()) == sorted(posts, key=lambda post: post.publish, reverse=True)

    def test_string_representation(self, post_factory):
        post = post_factory()
        assert str(post) == post.title
