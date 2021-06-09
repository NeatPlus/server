from django.contrib.gis.geos import GEOSGeometry
from django.core.files.storage import default_storage
from rest_framework import serializers
from rest_framework.fields import ImageField
from rest_framework_gis.fields import GeometryField

from neatplus.serializers import RichTextModelSerializer

from .models import (
    AnswerTypeChoices,
    Option,
    Question,
    QuestionGroup,
    Survey,
    SurveyAnswer,
)


class QuestionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionGroup
        fields = "__all__"


class QuestionSerializer(RichTextModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"


class SurveyAnswerSerializer(serializers.ModelSerializer):
    formatted_answer = serializers.SerializerMethodField()

    answer_type_serializer_mapping = {
        AnswerTypeChoices.BOOLEAN.value: serializers.BooleanField,
        AnswerTypeChoices.DATE.value: serializers.DateField,
        AnswerTypeChoices.DESCRIPTION.value: None,
        AnswerTypeChoices.IMAGE.value: serializers.ImageField,
        AnswerTypeChoices.LOCATION.value: GeometryField,
        AnswerTypeChoices.NUMBER.value: serializers.FloatField,
        AnswerTypeChoices.TEXT.value: serializers.CharField,
        AnswerTypeChoices.SINGLE_OPTION.value: None,
        AnswerTypeChoices.MULTIPLE_OPTION.value: None,
    }

    class Meta:
        model = SurveyAnswer
        fields = "__all__"

    def validate(self, attrs):
        data = super().validate(attrs)
        question_obj = data["question"]
        answer_type = data["answer_type"]
        options = data.get("options")
        if answer_type != question_obj.answer_type:
            raise serializers.ValidationError(
                {
                    "answer_type": "answer type of question and provided answer type doesn't matched"
                }
            )
        serializer_class = self.answer_type_serializer_mapping[answer_type]
        if serializer_class is None and data.get("answer") is not None:
            raise serializers.ValidationError(
                {"answer": "answer field cannot be present for answer type"}
            )
        if answer_type in [
            AnswerTypeChoices.SINGLE_OPTION.value,
            AnswerTypeChoices.MULTIPLE_OPTION.value,
        ]:
            if options is None:
                raise serializers.ValidationError(
                    {"options": "options should be present for answer type"}
                )
            for option in options:
                if option.question != question_obj:
                    raise serializers.ValidationError(
                        {"options": "Invalid option for question"}
                    )
            if (
                answer_type == AnswerTypeChoices.SINGLE_OPTION.value
                and len(options) != 1
            ):
                raise serializers.ValidationError(
                    {
                        "options": "only one option in list form is supported for question"
                    }
                )
        if serializer_class is None:
            pass
        elif serializer_class == GeometryField:
            try:
                serializer_class().run_validation(
                    GEOSGeometry(data["answer"], srid=4326)
                )
            except:
                raise serializers.ValidationError({"answer": "Invalid point field"})
        elif serializer_class == ImageField:
            try:
                with default_storage.open(data["answer"]) as file:
                    serializer_class().run_validation(file)
            except:
                raise serializers.ValidationError({"answer": "Invalid image answer"})
        else:
            serializer_class().run_validation(data["answer"])
        return data

    def get_formatted_answer(self, instance):
        serializer_class = self.answer_type_serializer_mapping[instance.answer_type]
        if serializer_class is None:
            return None
        elif serializer_class == GeometryField:
            return serializer_class().to_representation(
                GEOSGeometry(instance.answer, srid=4326)
            )
        elif serializer_class == ImageField:
            return self.context["request"].build_absolute_uri(
                default_storage.url(instance.answer)
            )
        else:
            return serializer_class().to_representation(instance.answer)


class WritableSurveyAnswerSerializer(SurveyAnswerSerializer):
    class Meta:
        model = SurveyAnswer
        exclude = ("survey",)


class WritableSurveySerializer(SurveySerializer):
    answers = WritableSurveyAnswerSerializer(many=True)

    class Meta:
        model = Survey
        exclude = ("project",)
