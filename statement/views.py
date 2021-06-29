from rest_framework import permissions, viewsets

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
    permission_classes = [permissions.IsAuthenticated]
    queryset = StatementTopic.objects.all()
    filterset_class = StatementTopicFilter


class StatementTagGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTagGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = StatementTagGroup.objects.all()
    filterset_class = StatementTagGroupFilter


class StatementTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = StatementTag.objects.all()
    filterset_class = StatementTagFilter


class StatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatementSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Statement.objects.all()
    filterset_class = StatementFilter


class MitigationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MitigationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Mitigation.objects.all()
    filterset_class = MitigationFilter


class OpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OpportunitySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Opportunity.objects.all()
    filterset_class = OpportunityFilter


class QuestionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionStatementSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = QuestionStatement.objects.all()
    filterset_class = QuestionStatementFilter


class OptionStatementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionStatementSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = OptionStatement.objects.all()
    filterset_class = OptionStatementFilter


class OptionMitigationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionMitigationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = OptionMitigation.objects.all()
    filterset_class = OptionMitigationFilter


class OptionOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OptionOpportunitySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = OptionOpportunity.objects.all()
    filterset_class = OptionOpportunityFilter
