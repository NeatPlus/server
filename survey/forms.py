from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import Question


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
        }
