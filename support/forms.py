from neatplus.forms import BaseCKEditorForm
from .models import LegalDocument, Action, EmailTemplate


class ActionAdminForm(BaseCKEditorForm):
    class Meta:
        model = Action
        fields = "__all__"
        ckeditor_fields = ["description"]


class EmailTemplateAdminForm(BaseCKEditorForm):
    class Meta:
        model = EmailTemplate
        fields = "__all__"
        ckeditor_fields = [("html_message", "basic")]


class LegalDocumentAdminForm(BaseCKEditorForm):
    class Meta:
        model = LegalDocument
        fields = "__all__"
        ckeditor_fields = ["description"]
