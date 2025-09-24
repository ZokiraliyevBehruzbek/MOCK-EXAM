from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define JWT Bearer security scheme
swagger_security = [{"Bearer": []}]

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # leave empty to use global DRF auth
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("auth/", include("users.urls")),
        path("exam/", include("Exam.urls")),
        path(
            "swagger(<format>\.json|\.yaml)",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        # path("movies/", include("movies.urls")),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
