from ckeditor_uploader.fields import RichTextUploadingField
from defender import config as defender_config
from defender import utils as defender_utils
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import inline_serializer
from rest_framework import exceptions, serializers
from rest_framework.fields import CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CKEDITOR_LOCATION = f"/{settings.MEDIA_LOCATION}/{settings.CKEDITOR_UPLOAD_PATH}"
ORIGINAL_TEXT = f'src="{CKEDITOR_LOCATION}'

UserModel = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    def build_relational_field(self, field_name, relation_info):
        if (
            relation_info.related_model == get_user_model()
            and relation_info.to_field is None
        ):
            relation_info = relation_info._replace(to_field="username")
        return super().build_relational_field(field_name, relation_info)


class ExcludeUserStampedFieldSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        if hasattr(self.Meta, "exclude"):
            excluded_fields = self.Meta.exclude
            if "created_by" not in excluded_fields:
                excluded_fields += ("created_by",)
            if "updated_by" not in excluded_fields:
                excluded_fields += ("updated_by",)
            self.Meta.exclude = excluded_fields
        elif hasattr(self.Meta, "fields"):
            fields = self.Meta.fields
            if type(fields, str):
                delattr(self.Meta, "fields")
                self.Meta.exclude = ("created_by", "updated_by")
            else:
                fields = list(fields)
                if "created_by" in fields:
                    fields.remove("created_by")
                if "updated_by" in fields:
                    fields.remove("updated_by")
                self.Meta.fields = tuple(fields)

        super().__init__(*args, **kwargs)


class RichTextUploadingSerializerField(CharField):
    def to_representation(self, value):
        data = super().to_representation(value)
        if not settings.USE_S3_STORAGE:
            replace_text = ORIGINAL_TEXT.replace(
                CKEDITOR_LOCATION,
                self.context["request"].build_absolute_uri(CKEDITOR_LOCATION),
            )
            data = data.replace(ORIGINAL_TEXT, replace_text)
        return data


class RichTextUploadingModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping[
            RichTextUploadingField
        ] = RichTextUploadingSerializerField
        super().__init__(*args, **kwargs)


class TokenObtainPairDefenderSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login_unsuccessful = False
        login_exception = None
        request_username = attrs[self.username_field]
        request = self.context["request"]

        try:
            data = super().validate(attrs)
        except exceptions.AuthenticationFailed as error:
            login_unsuccessful = True
            attempt_count = defender_utils.get_user_attempts(
                request, username=request_username
            )
            message = _(
                f"{error}. You have {defender_config.FAILURE_LIMIT-attempt_count-1} attempts remaining"
            )
            login_exception = exceptions.AuthenticationFailed(message)

        block_detail_message = _(
            "You have attempted to login {failure_limit} times with no success. Wait {cooloff_time_seconds} seconds to re login"
        ).format(
            failure_limit=defender_config.FAILURE_LIMIT,
            cooloff_time_seconds=defender_config.COOLOFF_TIME,
        )
        block_exception = exceptions.AuthenticationFailed(block_detail_message)

        if defender_utils.is_already_locked(request, username=request_username):
            raise block_exception

        defender_utils.add_login_attempt_to_db(
            request,
            login_valid=not login_unsuccessful,
            username=request_username,
        )
        user_not_blocked = defender_utils.check_request(
            request,
            login_unsuccessful=login_unsuccessful,
            username=request_username,
        )
        if user_not_blocked:
            if login_unsuccessful:
                raise login_exception
            else:
                return data
        else:
            raise block_exception


def get_detail_inline_serializer(name, content):
    return inline_serializer(
        name=name,
        fields={
            "detail": serializers.CharField(default=content),
        },
    )


def get_errors_inline_serializer(name):
    return inline_serializer(
        name=name,
        fields={"errors": serializers.DictField(child=serializers.CharField())},
    )
