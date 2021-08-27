from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class StaticStorage(S3StaticStorage):
    location = settings.STATIC_LOCATION
    default_acl = "public-read"


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIA_LOCATION
    default_acl = "private"
    file_overwrite = False


class CKEditorStorage(S3Boto3Storage):
    location = settings.MEDIA_LOCATION
    default_acl = "public-read"
    querystring_auth = False
    file_overwrite = False
