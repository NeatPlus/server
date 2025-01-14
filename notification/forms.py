from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Notice


class NoticeAdminForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
        }
