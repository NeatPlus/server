from rest_flex_fields import EXPAND_PARAM, WILDCARD_VALUES


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
