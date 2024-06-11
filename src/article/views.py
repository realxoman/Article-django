from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from article.models import Article
from article.serializers import ArticleListSerializer, ArticlePointSerializer


class ArticleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

    @action(detail=True, serializer_class=ArticlePointSerializer, methods=["POST"])
    def save_point(self, request, pk: int):
        article_object = self.get_object()
        point_serializer = ArticlePointSerializer(
            data=request.data,
            context=self.get_serializer_context()
        )
        point_serializer.is_valid(raise_exception=True)

        try:
            point_serializer.save(article=article_object, user=request.user)
        except ValidationError as e:
            return Response(e.get_full_details(), status=status.HTTP_403_FORBIDDEN)

        return Response(point_serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action == 'save_point':
            return [permissions.IsAuthenticatedOrReadOnly()]
        return super().get_permissions()
