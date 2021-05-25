from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from context.views import ContextViewSet, ModuleViewSet
from notification.views import NotificationViewSet
from organization.views import OrganizationViewSet
from project.views import ProjectViewSet
from support.views import FrequentlyAskedQuestionViewSet
from survey.views import OptionViewSet, QuestionGroupViewSet, QuestionViewSet
from user.views import UserViewSet

API_VERSION = "v1"


def get_api_path(path):
    return r"^api/(?P<version>({}))/{}".format(API_VERSION, path)


router = routers.DefaultRouter()
router.register("context", ContextViewSet, basename="context")
router.register(
    "frequently-asked-question",
    FrequentlyAskedQuestionViewSet,
    basename="frequently-asked-question",
)
router.register("module", ModuleViewSet, basename="module")
router.register("notification", NotificationViewSet, basename="notification")
router.register("option", OptionViewSet, basename="option")
router.register("organization", OrganizationViewSet, basename="organization")
router.register("project", ProjectViewSet, basename="project")
router.register("question-group", QuestionGroupViewSet, basename="question-group")
router.register("question", QuestionViewSet, basename="question")
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
    # silk
    re_path(r"^silk/", include("silk.urls", namespace="silk")),
    # DRF spectaular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]

if not settings.IS_SERVER_SECURE:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]

if not settings.USE_S3_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
