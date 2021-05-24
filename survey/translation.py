from modeltranslation import translator

from .models import Option, Question, QuestionGroup


@translator.register(QuestionGroup)
class QuestionGroupTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(Question)
class QuestionTranslationOptions(translator.TranslationOptions):
    fields = ("title", "description", "hints")


@translator.register(Option)
class OptionTranslationOptions(translator.TranslationOptions):
    fields = ("title",)
