from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class BaseCKEditorForm(forms.ModelForm):
    config_name = "default"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ckeditor_fields = getattr(self.Meta, "ckeditor_fields", [])

        if not isinstance(ckeditor_fields, (list, tuple)):
            ckeditor_fields = [ckeditor_fields]

        for field in ckeditor_fields:
            config = self.config_name
            if isinstance(field, tuple):
                field_name, config = field
            else:
                field_name = field

            if field_name and field_name in self.fields:
                self.fields[field_name].widget = CKEditor5Widget(config_name=config)
