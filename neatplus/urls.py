from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
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
    UserRegisterView,
)

API_VERSION = "v1"


def get_api_path(path):
    return r"^api/(?P<version>({}))/{}".format(API_VERSION, path)


if settings.IS_SERVER_SECURE:
    from django_otp.admin import OTPAdminSite

    class OTPAdmin(OTPAdminSite):
        pass

    admin.site.__class__ = OTPAdmin


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        get_api_path(r"jwt/create/$"), TokenObtainPairView.as_view(), name="jwt-create"
    ),
    re_path(
        get_api_path(r"jwt/refresh/$"), TokenRefreshView.as_view(), name="jwt-refresh"
    ),
    re_path(
        get_api_path(r"jwt/verify/$"), TokenVerifyView.as_view(), name="jwt-verify"
    ),
    re_path(
        get_api_path(r"registration/$"),
        UserRegisterView.as_view(),
        name="register",
    ),
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
    re_path(r"^silk/", include("silk.urls", namespace="silk")),
]

if not settings.IS_SERVER_SECURE:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]

if not settings.USE_S3_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
