from rest_framework import serializers

from .models import FrequentlyAskedQuestion


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        fields = "__all__"
