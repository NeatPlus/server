from modeltranslation import translator

from .models import Action, FrequentlyAskedQuestion, Resource


@translator.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionTranslationOptions(translator.TranslationOptions):
    fields = ("question", "answer")


@translator.register(Resource)
class ResourceTranslationOptions(translator.TranslationOptions):
    fields = ("title", "description")


@translator.register(Action)
class ActionTranslationOptions(translator.TranslationOptions):
    fields = ("title", "summary", "description")
