from neatplus.forms import BaseCKEditorForm
from .models import Notice


class NoticeAdminForm(BaseCKEditorForm):
    class Meta:
        model = Notice
        fields = "__all__"
        ckeditor_fields = ["description"]
