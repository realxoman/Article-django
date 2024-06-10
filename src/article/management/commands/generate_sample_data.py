import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from article.models import Article, Point

User = get_user_model()


class Command(BaseCommand):
    help_text = 'Generate sample data for testing'

    def handle(self, *args, **kwargs):
        # Create 500 users
        users = []
        for i in range(500):
            username = f'user{i+1}'
            users.append(User(username=username, password='password'))

        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS('500 users created'))

        # Create 10000 articles
        articles = []
        for i in range(10000):
            article = Article(title=f'Test Article3 {i + 1}', description=f'Test Description {i + 1}')
            articles.append(article)

        Article.objects.bulk_create(articles)
        self.stdout.write(self.style.SUCCESS('10000 articles created'))

        # Fetch all articles
        articles = list(Article.objects.all())

        # Fetch all users
        users = list(User.objects.all())

        # Generate around points
        points_created = 0
        points = []
        for article in articles:
            for user in users:
                point = random.randint(0, 5)
                points.append(Point(article=article, user=user, point=point))

            if len(points) >= 100000:
                Point.objects.bulk_create(points)
                points = []
                points_created += 100000
                self.stdout.write(self.style.SUCCESS(f'{points_created} points created'))
