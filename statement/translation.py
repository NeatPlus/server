from modeltranslation import translator

from .models import (
    Mitigation,
    Opportunity,
    Statement,
    StatementTag,
    StatementTagGroup,
    StatementTopic,
)


@translator.register(StatementTopic)
class StatementTopicTranslationOptions(translator.TranslationOptions):
    fields = ("title", "description")


@translator.register(StatementTagGroup)
class StatementTagGroupTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(StatementTag)
class StatementTagTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(Statement)
class StatementTranslationOptions(translator.TranslationOptions):
    fields = ("title", "hints")


@translator.register(Mitigation)
class MitigationTranslationOptions(translator.TranslationOptions):
    fields = ("title",)


@translator.register(Opportunity)
class OpportunityTranslationOptions(translator.TranslationOptions):
    fields = ("title",)
