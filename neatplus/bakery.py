from django.contrib.auth import get_user_model
from model_bakery.baker import Baker, random_gen

from neatplus.models import UserStampedModel


class UserStampedBaker(Baker):
    def _make(
        self,
        commit,
        commit_related,
        _save_kwargs,
        _refresh_after_create,
        _from_manager,
        **attrs
    ):
        self.passed_attrs = dict(attrs)
        return super()._make(
            commit=commit,
            commit_related=commit_related,
            _save_kwargs=_save_kwargs,
            _refresh_after_create=_refresh_after_create,
            _from_manager=_from_manager,
            **attrs
        )

    def instance(self, attrs, _commit, _save_kwargs, _from_manager):
        # if any field contains choice and unique reference then get first model if
        # field is not passed as parameter since model bakery cannot handle such case
        # properly
        for field in self.get_fields():
            try:
                if (
                    field.unique
                    and field.choices
                    and field.name not in self.passed_attrs
                ):
                    instance = self.model.objects.first()
                    if instance:
                        return instance
            # ignore attribute error while getting fields since some field may not have
            # desired attribute specially generic foreign key and many to many rel
            except AttributeError as _:
                pass
        # for userstampedmodel pass user model if field is missing
        if issubclass(self.model, UserStampedModel):
            created_by_field = attrs.get("created_by", None)
            if created_by_field is None:
                created_by_user = random_gen.gen_related(get_user_model())
                attrs["created_by"] = created_by_user
        return super().instance(attrs, _commit, _save_kwargs, _from_manager)
