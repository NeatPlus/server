from rest_framework import serializers

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


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"
