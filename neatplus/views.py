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
