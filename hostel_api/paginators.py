from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class MetaPaginator(LimitOffsetPagination):
    """
    Класс для пагинации вида
    {
        meta: {
            pagination: {
                limit: ...
                offset: ...
                total: ...
            }
        }

        data: [...]

    }
    """
    default_limit = 10

    def get_paginated_response(self, data):
        """ Создание ответа с пагинацией """
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
        """ Получение количества элементов на странице из тела запроса """
        pagination = request.data.get('pagination')
        if not pagination:
            return self.default_limit

        limit = pagination.get('limit')
        if limit is None:
            return self.default_limit

        return limit

    def get_offset(self, request):
        """ Получение отступа из тела запроса """
        pagination = request.data.get('pagination')
        if not pagination:
            return 0

        offset = pagination.get('offset')
        if offset is None:
            return 0

        return offset

