from django.test import TestCase
from django.contrib.auth import get_user_model

from article.models import Article, Point

User = get_user_model()


class ArticleModelTest(TestCase):

    def test_create_article(self):
        article = Article.objects.create(title="Test Title", description="Test Description")
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.description, "Test Description")
        self.assertEqual(article.average_points, 0)
        self.assertEqual(article.count_points, 0)

    def test_default_values(self):
        article = Article.objects.create()
        self.assertEqual(article.title, "Default Title")
        self.assertEqual(article.description, "Default Description")

    def test_calculate_average_points(self):
        article = Article.objects.create()
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')

        Point.objects.create(article=article, user=user1, point=3)
        Point.objects.create(article=article, user=user2, point=5)

        article.calculate_average_points()

        self.assertEqual(article.average_points, 4)
        self.assertEqual(article.count_points, 2)


class PointModelTest(TestCase):

    def setUp(self):
        self.article = Article.objects.create()
        self.article2 = Article.objects.create(title="Hi")
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

    def test_create_point(self):
        point = Point.objects.create(article=self.article, user=self.user1, point=3)
        self.assertEqual(point.article, self.article)
        self.assertEqual(point.user, self.user1)
        self.assertEqual(point.point, 3)

    def test_update_point(self):
        point = Point.objects.create(article=self.article, user=self.user1, point=3)
        point.point = 5
        point.save()

        point.refresh_from_db()
        self.assertEqual(point.point, 5)

        self.article.refresh_from_db()
        self.assertEqual(self.article.average_points, 5)

    def test_point_validators(self):
        with self.assertRaises(ValueError):
            Point.objects.create(article=self.article, user=self.user1, point=-1)

        with self.assertRaises(ValueError):
            Point.objects.create(article=self.article, user=self.user1, point=6)

    def test_update_article_points(self):
        point = Point.objects.create(article=self.article2, user=self.user1, point=2)
        self.article2.refresh_from_db()
        self.assertEqual(self.article2.average_points, 2)

        point.point = 4
        point.save()
        self.article2.refresh_from_db()
        self.assertEqual(self.article2.average_points, 4)

        Point.objects.create(article=self.article2, user=self.user2, point=3)
        self.article2.refresh_from_db()
        self.assertEqual(self.article2.average_points, 4)


if __name__ == '__main__':
    TestCase.main()
