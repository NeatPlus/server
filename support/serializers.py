from rest_framework import serializers

from neatplus.serializers import RichTextUploadingModelSerializer

from .models import (
    Action,
    FrequentlyAskedQuestion,
    LegalDocument,
    Resource,
    ResourceTag,
)


class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = "__all__"


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        fields = "__all__"


class ResourceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceTag
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class ActionSerializer(RichTextUploadingModelSerializer):
    context_title = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = "__all__"

    def get_context_title(self, instance):
        if instance.context:
            return instance.context.title
