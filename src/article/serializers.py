from contextlib import suppress

from django.core.cache import cache
from django.conf import settings

from rest_framework import serializers

from article.models import Article, Point


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'points']

    points = serializers.SerializerMethodField()

    def get_points(self, obj: Article):
        cache_key_avg = f'article_{obj.id}_avg'
        cache_key_count = f'article_{obj.id}_count'
        if obj.average_points == 0:
            obj.calculate_average_points()

        request = self.context.get('request')
        user_point = None
        with suppress(Exception):  # Use suppress to ignore exceptions
            if request.user.is_authenticated:
                user_point: Point = obj.point_article.filter(user=request.user).first()

        if cache.get(cache_key_avg):
            average_score = cache.get(cache_key_avg)
            ratings_count = cache.get(cache_key_count)
        else:
            average_score = obj.average_points
            ratings_count = obj.count_points
            cache.set(cache_key_avg, average_score, settings.CACHE_TIME)
            cache.set(cache_key_count, ratings_count, settings.CACHE_TIME)

        context = {
            "number_of_points": ratings_count,
            "average_point": average_score,
            "user_point": user_point.point if user_point else None
        }
        return context


class ArticlePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['point']

    def save(self, **kwargs):
        article = kwargs.get('article')
        user = kwargs.get('user')
        cache_key_count = f'article_{article.id}_count_force'

        if cache.get(cache_key_count):
            if cache.get(cache_key_count) >= settings.CACHE_LIMIT:
                raise serializers.ValidationError("Flood Detected. Try Again Later")
            else:
                cache.incr(cache_key_count)
        else:
            cache.set(cache_key_count, 1, settings.CACHE_TIME)

        # Call the parent class's save method with validated data
        super().save(article=article, user=user)
