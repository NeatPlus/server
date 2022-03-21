from neatplus.serializers import UserModelSerializer

from .models import Context, Module


class ContextSerializer(UserModelSerializer):
    class Meta:
        model = Context
        fields = "__all__"


class ModuleSerializer(UserModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"
