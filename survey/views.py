from rest_framework import viewsets

from neatplus.views import UserStampedModelViewSetMixin

from .filters import OptionFilter, QuestionFilter
from .models import Option, Question, QuestionGroup
from .serializers import OptionSerializer, QuestionGroupSerializer, QuestionSerializer


class QuestionGroupViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = QuestionGroupSerializer
    queryset = QuestionGroup.objects.all()


class QuestionViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filterset_class = QuestionFilter


class OptionViewSet(UserStampedModelViewSetMixin, viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    filterset_class = OptionFilter
