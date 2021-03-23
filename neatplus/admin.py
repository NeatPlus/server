from django.contrib import admin


class UserStampedModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
