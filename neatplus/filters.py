from django.db.models import Q
from django_filters import BaseInFilter, ModelChoiceFilter


class M2MInFilter(BaseInFilter, ModelChoiceFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        if value != self.null_value:
            q = Q()
            for v in set(value):
                predicate = {f"{self.field_name}": v}
                q |= Q(**predicate)
            queryset = self.get_method(qs)(q)
            return queryset.distinct() if self.distinct else queryset

        return qs.distinct() if self.distinct else qs
