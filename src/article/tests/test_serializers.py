from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from unittest.mock import patch

from article.serializers import ArticlePointSerializer
from article.models import Article

User = get_user_model()


class ArticlePointSerializerTestCase(TestCase):
    def setUp(self):
        # Create some dummy data for testing
        self.article = Article.objects.create(title="Test Article")
        self.user = User.objects.create(username="testuser")

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.incr')
    @patch('django.core.cache.cache.set')
    def test_cache_limit_enforced(self, mock_cache_set, mock_cache_incr, mock_cache_get):
        # Mocking cache behavior
        mock_cache_get.return_value = settings.CACHE_LIMIT - 1  # Below cache limit
        serializer = ArticlePointSerializer(data={'point': 5})

        # Call serializer's save method
        serializer.is_valid()
        serializer.save(article=self.article, user=self.user)

        # Ensure cache methods were called with correct arguments
        mock_cache_incr.assert_called_once_with(f'article_{self.article.id}_count_force')
        mock_cache_set.assert_not_called()  # Cache set should not be called since limit is not exceeded

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.incr')
    @patch('django.core.cache.cache.set')
    def test_cache_limit_exceeded(self, mock_cache_set, mock_cache_incr, mock_cache_get):
        # Mocking cache behavior to exceed the limit
        mock_cache_get.return_value = settings.CACHE_LIMIT  # At cache limit
        serializer = ArticlePointSerializer(data={'point': 5})

        # Call serializer's save method
        serializer.is_valid()
        with self.assertRaises(ValidationError):
            serializer.save(article=self.article, user=self.user)

        # Ensure cache methods were called with correct arguments
        mock_cache_incr.assert_not_called()  # Cache increment should not be called since limit is exceeded
        mock_cache_set.assert_not_called()  # Cache set should not be called since limit is exceeded
