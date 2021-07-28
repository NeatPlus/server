from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from .models import LegalDocument, LegalDocumentTypeChoice


@receiver(post_save, sender=LegalDocument)
def update_user_terms_and_privacy_acceptance_status(
    sender, instance, created, **kwargs
):
    update_fields = kwargs.get("update_fields")
    if (
        created or (update_fields and "description" in update_fields)
    ) and instance.document_type in [
        LegalDocumentTypeChoice.TERMS_AND_CONDITIONS,
        LegalDocumentTypeChoice.PRIVACY_POLICY,
    ]:
        get_user_model().objects.all().update(
            has_accepted_terms_and_privacy_policy=False
        )
