from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class MetaPaginator(LimitOffsetPagination):
    default_limit = 10

    def get_paginated_response(self, data):
        pagination = {
            "pagination": {
                "limit": self.limit,
                "offset": self.offset,
                "total": self.count
            }
        }
        return Response(OrderedDict([
            ('meta', pagination),
            ('data', data)
        ]))

    def get_limit(self, request):
        pagination = request.data.get('pagination')
        if not pagination:
            return self.default_limit

        limit = pagination.get('limit')
        if limit is None:
            return self.default_limit

        return limit

    def get_offset(self, request):
        pagination = request.data.get('pagination')
        if not pagination:
            return 0

        offset = pagination.get('offset')
        if offset is None:
            return 0

        return offset

