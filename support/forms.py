from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import LegalDocument, Action, EmailTemplate


class ActionAdminForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
        }


class EmailTemplateAdminForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = "__all__"
        widgets = {
            "html_message": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
        }


class LegalDocumentAdminForm(forms.ModelForm):
    class Meta:
        model = LegalDocument
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
        }
