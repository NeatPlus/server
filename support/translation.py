from modeltranslation import translator

from .models import FrequentlyAskedQuestion


@translator.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionTranslationOptions(translator.TranslationOptions):
    fields = ("question", "answer")
