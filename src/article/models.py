from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from shared.models import BaseModel


class Article(BaseModel):
    """
    Article model
    --------------------------------
    title: str - max-256
    description: text
    --------------------------------
    """

    title = models.CharField(max_length=256, default="Default Title")
    description = models.TextField(default="Default Description")


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

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    point = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        if self.pk is None:
            existing_point = Point.objects.filter(article=self.article, user=self.user).first()
            if existing_point:
                # Update the existing point instead of creating a new one
                existing_point.point = self.point
                existing_point.save()
                return

        # Call the original save method
        super(Point, self).save(*args, **kwargs)
