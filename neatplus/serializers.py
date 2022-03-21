from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

CKEDITOR_LOCATION = f"/{settings.MEDIA_LOCATION}/{settings.CKEDITOR_UPLOAD_PATH}"
ORIGINAL_TEXT = f'src="{CKEDITOR_LOCATION}'

UserModel = get_user_model()


class UserModelSerializer(ModelSerializer):
    def build_relational_field(self, field_name, relation_info):
        if (
            relation_info.related_model == get_user_model()
            and relation_info.to_field is None
        ):
            relation_info = relation_info._replace(to_field="username")
        return super().build_relational_field(field_name, relation_info)


class ExcludeUserStampedFieldSerializer(ModelSerializer):
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


class RichTextUploadingModelSerializer(UserModelSerializer):
    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping[
            RichTextUploadingField
        ] = RichTextUploadingSerializerField
        super().__init__(*args, **kwargs)
