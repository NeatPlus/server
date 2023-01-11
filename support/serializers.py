from rest_framework import serializers

from neatplus.serializers import RichTextUploadingModelSerializer, UserModelSerializer

from .models import (
    Action,
    FrequentlyAskedQuestion,
    LegalDocument,
    Resource,
    ResourceTag,
)


class LegalDocumentSerializer(UserModelSerializer):
    class Meta:
        model = LegalDocument
        fields = "__all__"


class FrequentlyAskedQuestionSerializer(UserModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        fields = "__all__"


class ResourceTagSerializer(UserModelSerializer):
    class Meta:
        model = ResourceTag
        fields = "__all__"


class ResourceSerializer(UserModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class ActionSerializer(RichTextUploadingModelSerializer, UserModelSerializer):
    context_title = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = "__all__"

    def get_context_title(self, instance):
        if instance.context:
            return instance.context.title
