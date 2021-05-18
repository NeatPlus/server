from modeltranslation import translator

from .models import Answer, Context, Module, Question, QuestionCategory


@translator.register(Context)
class ContextTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(Module)
class ModuleTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(QuestionCategory)
class QuestionCategoryTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(Question)
class QuestionTranslationOptions(translator.TranslationOptions):
    fields = ("title", "hints")


@translator.register(Answer)
class AnswerTranslationOptions(translator.TranslationOptions):
    fields = ("title",)
