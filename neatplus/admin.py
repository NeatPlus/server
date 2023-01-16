import csv

from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


class UserStampedModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


class AcceptRejectModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.model_name = model.__name__
        super().__init__(model, admin_site)

    def response_change(self, request, obj):
        if "_reject" in request.POST:
            obj.status = "rejected"
            obj.save()
            self.message_user(
                request, _("{name} rejected").format(name=self.model_name)
            )
            return HttpResponseRedirect(".")
        if "_accept" in request.POST:
            obj.status = "accepted"
            obj.save()
            self.message_user(
                request, _("{name} accepted").format(name=self.model_name)
            )
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta.model_name}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row_values = []
            for field in field_names:
                field_value = getattr(obj, field)
                value = None
                if field == models.ForeignKey or models.OneToOneField:
                    if field_value:
                        value = str(field_value)
                elif field == models.ManyToManyField:
                    value = []
                    if field_value:
                        for val in field_value:
                            value.append(str(val))
                if value is None:
                    value = field_value
                row_values.append(value)
            row = writer.writerow(row_values)

        return response

        export_as_csv.short_description = "Export Selected row"
