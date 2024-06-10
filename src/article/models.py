from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg

from shared.models import BaseModel


class Article(BaseModel):
    """
    Article model
    --------------------------------
    title: str - max-256
    description: text
    --------------------------------
    """

    title = models.CharField(max_length=256, default="Default Title", unique=True)
    description = models.TextField(default="Default Description")
    average_points = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    count_points = models.PositiveIntegerField(default=0)

    def calculate_average_points(self):
        point_objects = self.point_article.values('point').aggregate(Avg('point'), Count('point'))
        self.average_points = round(point_objects['point__avg'] or 0)
        self.count_points = point_objects['point__count']
        self.save()


class Point(BaseModel):
    """
    Point model
    --------------------------------
    article: Foreign key
    user: Foreign key
    point: Uint8
    --------------------------------
    """

    class Meta:
        unique_together = ["article", "user"]

    article = models.ForeignKey(Article, related_name="point_article", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="point_user", on_delete=models.CASCADE)
    point = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        existing_point = Point.objects.filter(article=self.article, user=self.user).first()
        if existing_point:
            # Update the existing point instead of creating a new one
            old_point = existing_point.point
            existing_point.point = self.point
            Point.objects.filter(id=existing_point.id).update(point=self.point)
            self.update_article_points(old_point)
            return

        # Call the original save method
        super(Point, self).save(*args, **kwargs)
        self.update_article_points()

    def update_article_points(self, old_point=None):
        if old_point is not None:
            # Calculate the correct average when updating an existing point
            sum_of_points = (self.article.average_points * self.article.count_points) - old_point + self.point
        else:
            # Calculate the correct average when adding a new point
            sum_of_points = (self.article.average_points * self.article.count_points) + self.point
            self.article.count_points += 1

        self.article.average_points = round(sum_of_points / self.article.count_points)
        self.article.save()
