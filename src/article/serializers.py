from django.core.cache import cache

from rest_framework import serializers

from article.models import Article, Point


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'points']

    points = serializers.SerializerMethodField()

    def get_points(self, obj: Article):
        cache_key_avg = f'post_{obj.id}_avg'
        cache_key_count = f'post_{obj.id}_count'
        if obj.average_points == 0:
            obj.calculate_average_points()

        request = self.context.get('request')
        user_point = None
        if request.user.is_authenticated:
            user_point: Point = obj.point_article.filter(user=request.user).first()

        if cache.get(cache_key_avg):
            average_score = cache.get(cache_key_avg)
            ratings_count = cache.get(cache_key_count)
        else:
            average_score = obj.average_points
            ratings_count = obj.count_points
            cache.set(cache_key_avg, average_score, 60)
            cache.set(cache_key_count, ratings_count, 60)

        context = {
            "number_of_points": average_score,
            "average_point": ratings_count,
            "user_point": user_point.point if user_point else None
        }
        return context


class ArticlePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['point']
