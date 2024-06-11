from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from article.models import Article, Point
from article.serializers import ArticleListSerializer

User = get_user_model()


class ArticleViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.article = Article.objects.create(title="Test Article", description="Test Description")

    def test_list_articles(self):
        response = self.client.get(reverse('article_list-list'))
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_post_point_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('article_list-save-point', kwargs={'pk': self.article.pk})
        data = {'point': 4}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['point'], 4)

        # Check if the point is saved correctly
        point = Point.objects.get(article=self.article, user=self.user)
        self.assertEqual(point.point, 4)
        self.article.refresh_from_db()
        self.assertEqual(self.article.average_points, 4)

    def test_post_point_unauthenticated(self):
        url = reverse('article_list-save-point', kwargs={'pk': self.article.pk})
        data = {'point': 4}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_point_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('article_list-save-point', kwargs={'pk': self.article.pk})
        data = {'point': 6}  # Invalid point, as it exceeds the max value

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('point', response.data)


if __name__ == '__main__':
    import unittest
    unittest.main()
