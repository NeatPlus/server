from rest_framework import viewsets

from .filters import (
    MitigationFilter,
    OpportunityFilter,
    OptionMitigationFilter,
    OptionOpportunityFilter,
    OptionStatementFilter,
    QuestionStatementFilter,
    StatementFilter,
    StatementTagFilter,
    StatementTagGroupFilter,
    StatementTopicFilter,
)
from .models import (
    Mitigation,
    Opportunity,
    OptionMitigation,
    OptionOpportunity,
    OptionStatement,
    QuestionStatement,
    Statement,
    StatementTag,
    StatementTagGroup,
    StatementTopic,
)
from .serializers import (
    MitigationSerializer,
    OpportunitySerializer,
    OptionMitigationSerializer,
    OptionOpportunitySerializer,
    OptionStatementSerializer,
    QuestionStatementSerializer,
    StatementSerializer,
    StatementTagGroupSerializer,
    StatementTagSerializer,
    StatementTopicSerializer,
)


class StatementTopicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTopicSerializer
    queryset = StatementTopic.objects.all()
    filterset_class = StatementTopicFilter


class StatementTagGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTagGroupSerializer
    queryset = StatementTagGroup.objects.all()
    filterset_class = StatementTagGroupFilter


class StatementTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTagSerializer
    queryset = StatementTag.objects.all()
    filterset_class = StatementTagFilter


class StatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementSerializer
    queryset = Statement.objects.all()
    filterset_class = StatementFilter


class MitigationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MitigationSerializer
    queryset = Mitigation.objects.all()
    filterset_class = MitigationFilter


class OpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OpportunitySerializer
    queryset = Opportunity.objects.all()
    filterset_class = OpportunityFilter


class QuestionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionStatementSerializer
    queryset = QuestionStatement.objects.all()
    filterset_class = QuestionStatementFilter


class OptionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionStatementSerializer
    queryset = OptionStatement.objects.all()
    filterset_class = OptionStatementFilter


class OptionMitigationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionMitigationSerializer
    queryset = OptionMitigation.objects.all()
    filterset_class = OptionMitigationFilter


class OptionOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionOpportunitySerializer
    queryset = OptionOpportunity.objects.all()
    filterset_class = OptionOpportunityFilter
