from django.urls import include, path
from rest_framework import routers

from article.views import ArticleViewSet


router = routers.DefaultRouter()
router.register("", ArticleViewSet, basename="article_list")

urlpatterns = [
    path("", include(router.urls)),
]
