from django.contrib.auth import get_user_model
from model_bakery.baker import Baker, random_gen

from neatplus.models import UserStampedModel


class UserStampedBaker(Baker):
    def instance(self, attrs, _commit, _save_kwargs, _from_manager):
        if issubclass(self.model, UserStampedModel):
            created_by_field = attrs.get("created_by", None)
            if created_by_field is None:
                created_by_user = random_gen.gen_related(get_user_model())
                attrs["created_by"] = created_by_user
        return super().instance(attrs, _commit, _save_kwargs, _from_manager)
