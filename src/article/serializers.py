from rest_framework import serializers

from article.models import Article, Point


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'points']

    points = serializers.SerializerMethodField()

    def get_points(self, obj: Article):
        if obj.average_points == 0:
            obj.calculate_average_points()

        request = self.context.get('request')
        user_point = None
        if request.user.is_authenticated:
            user_point: Point = obj.point_article.filter(user=request.user).first()

        context = {
            "number_of_points": obj.count_points,
            "average_point": obj.average_points,
            "user_point": user_point.point if user_point else None
        }
        return context


class ArticlePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['point']
