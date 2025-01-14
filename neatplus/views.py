from rest_flex_fields import EXPAND_PARAM, WILDCARD_VALUES

# modules for custom file upload handling
from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserStampedModelCreateMixin:
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserStampedModelUpdateMixin:
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class UserStampedModelViewSetMixin(
    UserStampedModelCreateMixin, UserStampedModelUpdateMixin
):
    pass


class RetrieveRelatedObjectMixin:
    def fetch_related_objects(self, queryset):
        if self.action == "list":
            expand_params = self.request.query_params.get(EXPAND_PARAM, "").split(",")
            wildcard_present = any(value in expand_params for value in WILDCARD_VALUES)
            if hasattr(self, "expand_prefetch_fields"):
                for field in self.expand_prefetch_fields:
                    if field in expand_params or wildcard_present:
                        queryset = queryset.prefetch_related(field)
            if hasattr(self, "expand_select_fields"):
                for field in self.expand_select_fields:
                    if field in expand_params or wildcard_present:
                        queryset = queryset.select_related(field)
        return queryset



def ckeditor_file_upload_view(request):
     if request.method == "POST" and 'upload' in request.FILES:
         # Retrieve the uploaded file
         uploaded_file = request.FILES['upload']
         file_path = default_storage.save(f"ckeditor/{uploaded_file.name}", uploaded_file)
         file_url = default_storage.url(file_path)

         # Return the JSON response with the file URL
         return JsonResponse({
             "url": file_url,
             "message": "File uploaded successfully!",
         })

     # If no file is uploaded or the request method is not POST
     return JsonResponse({
         "error": "No file uploaded or invalid request method.",
     }, status=400)

