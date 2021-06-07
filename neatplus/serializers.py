from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

CKEDITOR_LOCATION = f"/{settings.MEDIA_LOCATION}/{settings.CKEDITOR_UPLOAD_PATH}"
ORIGINAL_TEXT = f'src="{CKEDITOR_LOCATION}'


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


class RichTextModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping[
            RichTextUploadingField
        ] = RichTextUploadingSerializerField
        super().__init__(*args, **kwargs)
