from django.db.models import Count, Avg

from rest_framework import serializers

from article.models import Article, Point


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'points']

    points = serializers.SerializerMethodField()

    def get_points(self, obj):
        point_object = obj.point_article.values('point').aggregate(Avg('point'), Count('point'))

        request = self.context.get('request')
        user_point = None
        if request.user.is_authenticated:
            user_point = obj.point_article.filter(user=request.user).first()

        context = {
            "number_of_points": point_object['point__count'],
            "average_point": point_object['point__avg'] or 0,
            "user_point": user_point.point if user_point else None
        }
        return context


class ArticlePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['point']
