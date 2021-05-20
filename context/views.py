from rest_framework import viewsets

from .models import Context, Module
from .serializers import ContextSerializer, ModuleSerializer


class ContextViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
