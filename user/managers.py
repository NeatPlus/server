from django.contrib.auth.models import UserManager
from django.db.models import Q


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(Q(username__iexact=username) | Q(email__iexact=username))

    def filter_by_username(self, username, **kwargs):
        return self.filter(
            Q(username__iexact=username) | Q(email__iexact=username), **kwargs
        )
