from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

API_VERSION = "v1"


def get_api_path(path):
    return r"^api/(?P<version>({}))/{}".format(API_VERSION, path)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    re_path(
        get_api_path(r"jwt/create/$"), TokenObtainPairView.as_view(), name="jwt-create"
    ),
    re_path(
        get_api_path(r"jwt/refresh/$"), TokenRefreshView.as_view(), name="jwt-refresh"
    ),
    re_path(
        get_api_path(r"jwt/verify/$"), TokenVerifyView.as_view(), name="jwt-verify"
    ),
]
