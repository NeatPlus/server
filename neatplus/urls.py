from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    EmailConfirmPinSendView,
    EmailConfirmPinVerifyView,
    PasswordResetPasswordChangeView,
    PasswordResetPinSendView,
    PasswordResetPinVerifyView,
    UserViewSet,
)

API_VERSION = "v1"


def get_api_path(path):
    return r"^api/(?P<version>({}))/{}".format(API_VERSION, path)


router = routers.DefaultRouter()
router.register("user", UserViewSet, basename="user")

if settings.IS_SERVER_SECURE:
    from django_otp.admin import OTPAdminSite

    class OTPAdmin(OTPAdminSite):
        pass

    admin.site.__class__ = OTPAdmin


urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # DRF router
    re_path(get_api_path(""), include(router.urls)),
    # jwt
    re_path(
        get_api_path(r"jwt/create/$"), TokenObtainPairView.as_view(), name="jwt-create"
    ),
    re_path(
        get_api_path(r"jwt/refresh/$"), TokenRefreshView.as_view(), name="jwt-refresh"
    ),
    re_path(
        get_api_path(r"jwt/verify/$"), TokenVerifyView.as_view(), name="jwt-verify"
    ),
    # password reset
    re_path(
        get_api_path(r"password-reset-pin/$"),
        PasswordResetPinSendView.as_view(),
        name="password-reset-pin",
    ),
    re_path(
        get_api_path(r"password-reset-pin/verify/$"),
        PasswordResetPinVerifyView.as_view(),
        name="password-reset-pin-verify",
    ),
    re_path(
        get_api_path(r"password-reset-pin/change/$"),
        PasswordResetPasswordChangeView.as_view(),
        name="password-reset-pin-confirm",
    ),
    # email confirm
    re_path(
        get_api_path(r"email-confirm/$"),
        EmailConfirmPinSendView.as_view(),
        name="email-confirm",
    ),
    re_path(
        get_api_path(r"email-confirm/verify/$"),
        EmailConfirmPinVerifyView.as_view(),
        name="email-confirm-verify",
    ),
    # silk
    re_path(r"^silk/", include("silk.urls", namespace="silk")),
]

if not settings.IS_SERVER_SECURE:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]

if not settings.USE_S3_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
