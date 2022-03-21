from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from neatplus.serializers import UserModelSerializer

from .models import Notice, Notification


class NotificationSerializer(UserModelSerializer):
    actor_content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field="model",
    )
    target_content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field="model",
    )
    action_object_content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field="model",
    )
    actor_obj_str = serializers.SerializerMethodField()
    target_obj_str = serializers.SerializerMethodField()
    action_object_obj_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_actor_obj_str(self, instance):
        if instance.actor_content_object:
            return str(instance.actor_content_object)
        else:
            None

    def get_target_obj_str(self, instance):
        if instance.target_content_object:
            return str(instance.target_content_object)
        else:
            None

    def get_action_object_obj_str(self, instance):
        if instance.action_object_content_object:
            return str(instance.action_object_content_object)
        else:
            None


class UnReadCountResponseSerializer(serializers.Serializer):
    unread_count = serializers.IntegerField()


class NoticeSerializer(UserModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"
