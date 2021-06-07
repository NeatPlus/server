from rest_framework import serializers

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
    class Meta:
        model = Action
        fields = "__all__"
