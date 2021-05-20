from modeltranslation import translator

from .models import Context, Module


@translator.register(Context)
class ContextTranslationOptions(translator.TranslationOptions):
    fields = ("title", "description")


@translator.register(Module)
class ModuleTranslationOptions(translator.TranslationOptions):
    fields = ("title", "description")
