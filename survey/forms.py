from neatplus.forms import BaseCKEditorForm
from .models import Question


class QuestionAdminForm(BaseCKEditorForm):
    class Meta:
        model = Question
        fields = "__all__"
        ckeditor_fields = [
            "description",
            "description_en",
            "description_es",
            "description_fr",
        ]
