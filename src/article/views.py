from rest_framework import viewsets, mixins

from article.models import Article
from article.serializers import ArticleListSerializer


class ArticleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
