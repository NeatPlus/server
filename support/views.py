from rest_framework import viewsets

from .models import FrequentlyAskedQuestion
from .serializers import FrequentlyAskedQuestionSerializer


class FrequentlyAskedQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FrequentlyAskedQuestion.objects.all()
    serializer_class = FrequentlyAskedQuestionSerializer
