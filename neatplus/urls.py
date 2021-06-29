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
from organization.views import OrganizationMemberRequestViewSet, OrganizationViewSet
from project.views import ProjectViewSet
from statement.views import (
    MitigationViewSet,
    OpportunityViewSet,
    OptionMitigationViewSet,
    OptionOpportunityViewSet,
    OptionStatementViewSet,
    QuestionStatementViewSet,
    StatementTagGroupViewSet,
    StatementTagViewSet,
    StatementTopicViewSet,
    StatementViewSet,
)
from summary.views import SurveyResultViewSet
from support.views import (
    ActionViewSet,
    FrequentlyAskedQuestionViewSet,
    ResourceTagViewSet,
    ResourceViewSet,
)
from survey.views import (
    OptionViewSet,
    QuestionGroupViewSet,
    QuestionViewSet,
    SurveyAnswerViewSet,
    SurveyViewSet,
)
from user.views import UserViewSet

API_VERSION = "v1"


def get_api_path(path):
    return r"^api/(?P<version>({}))/{}".format(API_VERSION, path)


router = routers.DefaultRouter()
router.register("action", ActionViewSet, basename="action")
router.register("context", ContextViewSet, basename="context")
router.register(
    "frequently-asked-question",
    FrequentlyAskedQuestionViewSet,
    basename="frequently-asked-question",
)
router.register("mitigation", MitigationViewSet, basename="mitigation")
router.register("module", ModuleViewSet, basename="module")
router.register("notification", NotificationViewSet, basename="notification")
router.register("opportunity", OpportunityViewSet, basename="opportunity")
router.register("option", OptionViewSet, basename="option")
router.register(
    "option-mitigation", OptionMitigationViewSet, basename="option-mitigation"
)
router.register(
    "option-opportunity", OptionOpportunityViewSet, basename="option-opportunity"
)
router.register("option-statement", OptionStatementViewSet, basename="option-statement")
router.register("organization", OrganizationViewSet, basename="organization")
router.register(
    "organization-member-request",
    OrganizationMemberRequestViewSet,
    basename="organization-member-request",
)
router.register("project", ProjectViewSet, basename="project")
router.register("question", QuestionViewSet, basename="question")
router.register("question-group", QuestionGroupViewSet, basename="question-group")
router.register(
    "question-statement", QuestionStatementViewSet, basename="question-statement"
)
router.register("resource", ResourceViewSet, basename="resource")
router.register("resource-tag", ResourceTagViewSet, basename="resource-tag")
router.register("statement", StatementViewSet, basename="statement")
router.register("statement-tag", StatementTagViewSet, basename="statement-tag")
router.register(
    "statement-tag-group", StatementTagGroupViewSet, basename="statement-tag-group"
)
router.register("statement-topic", StatementTopicViewSet, basename="statement-topic")
router.register("survey", SurveyViewSet, basename="survey")
router.register("survey-answer", SurveyAnswerViewSet, basename="survey-answer")
router.register("survey-result", SurveyResultViewSet, basename="survey-result")
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
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

if not settings.IS_SERVER_SECURE:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]

if not settings.USE_S3_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
