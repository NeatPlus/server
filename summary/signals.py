from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from summary.models import SurveyResult


@receiver(post_save, sender=SurveyResult)
def update_baseline_feedback(sender, instance, created, **kwargs):
    update_fields = kwargs.get("update_fields")
    if update_fields and "score" in update_fields:
        feedbacks = instance.feedbacks.all()
        for feedback in feedbacks:
            if feedback.is_baseline:
                feedback.actual_score = instance.score
                feedback.save()
