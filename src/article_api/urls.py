from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Api routes
urlpatterns_api_v1 = [
    path("auth/", include("rest_framework.urls")),
    path("article/", include("article.urls")),
]

# Application routes
urlpatterns = [
    path('api/v1/', include(urlpatterns_api_v1), name="api_urls"),
    path('schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
