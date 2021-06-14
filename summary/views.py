from rest_framework import viewsets

from .models import Mitigation, Opportunity, Statement, StatementTopic
from .serializers import (
    MitigationSerializer,
    OpportunitySerializer,
    StatementSerializer,
    StatementTopicSerializer,
)


class StatementTopicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTopicSerializer
    queryset = StatementTopic.objects.all()


class StatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementSerializer
    queryset = Statement.objects.all()


class MitigationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MitigationSerializer
    queryset = Mitigation.objects.all()


class OpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()
