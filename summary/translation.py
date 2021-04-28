from modeltranslation import translator

from .models import Mitigation, Opportunity, Statement


@translator.register(Statement)
class StatementTranslationOptions(translator.TranslationOptions):
    fields = ("title", "hints")


@translator.register(Mitigation)
class MitigationTranslationOptions(translator.TranslationOptions):
    fields = ("title", "hints")


@translator.register(Opportunity)
class OpportunityTranslationOptions(translator.TranslationOptions):
    fields = ("title", "hints")
