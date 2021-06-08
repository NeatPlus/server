from rest_framework import serializers

from context.models import Context
from neatplus.serializers import RichTextModelSerializer

from .models import Action, FrequentlyAskedQuestion, Resource, ResourceTag


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


class ActionSerializer(RichTextModelSerializer):
    context_title = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = "__all__"

    def get_context_title(self, instance):
        if instance.context:
            return instance.context.title
