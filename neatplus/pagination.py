import sys

from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_limit(self, request):
        limit = request.query_params.get(self.limit_query_param, None)
        if limit:
            if int(limit) < 0:
                return sys.maxsize
            else:
                return int(limit)
        return self.default_limit
