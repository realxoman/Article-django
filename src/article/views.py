from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response


from article.models import Article
from article.serializers import ArticleListSerializer, ArticlePointSerializer


class ArticleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

    @action(detail=True, serializer_class=ArticlePointSerializer, methods=["POST"])
    def save_point(self, request, pk: int):
        if request.user.is_authenticated:
            article_object = self.get_object()
            point_serializer = ArticlePointSerializer(
                data=request.data,
                context=self.get_serializer_context()
            )
            point_serializer.is_valid(raise_exception=True)
            point_serializer.save(article=article_object, user=request.user)

            return Response(point_serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = "Guest users cannot rate articles"
            context = {"error_message": message}
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)
