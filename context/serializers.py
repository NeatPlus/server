from rest_framework import serializers

from .models import Context, Module


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"
