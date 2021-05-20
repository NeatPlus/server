from modeltranslation import translator

from .models import Answer, Question, QuestionCategory


@translator.register(QuestionCategory)
class QuestionCategoryTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(Question)
class QuestionTranslationOptions(translator.TranslationOptions):
    fields = ("title", "hints")


@translator.register(Answer)
class AnswerTranslationOptions(translator.TranslationOptions):
    fields = ("title",)
