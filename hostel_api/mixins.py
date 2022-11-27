from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.core import exceptions

from .paginators import MetaPaginator
from .exceptions import BadSearch


class DefaultViewMixin(ModelViewSet):
    """ Миксин для реализации поиска объектов """
    model = None
    model = None
    default_sort_fields = []
    default_filter_fields = {}
    default_include_fields = []
    pagination_class = MetaPaginator

    def search_filter(self, filter_: str, include: list, order_by: list):
        raise BadSearch({
            'error': 'Переданы некорректные поля, проверьте тело запроса.',
            'msg': 'Для этой модели не определен поиск'
        })

    def get_queryset(self):
        """ Получение queryset'a с заданной фильтрацией, сортировкой, включением нужных связанных объектов"""
        data = self.request.data
        order_by = data.get('sort')
        if not order_by:
            order_by = self.default_sort_fields
        filter_fields = data.get('filter', self.default_filter_fields)
        filter_ = data.get('search')

        if filter_ and filter_fields:
            return Response(data={
                'error': 'Переданы некорректные поля, проверьте тело запроса.',
                'msg': 'Нельзя использовать filter и search в одном запросе'
            }, status=status.HTTP_400_BAD_REQUEST)

        if filter_:
            return self.search_filter(filter_, self.request.data.get('include', []), order_by)

        else:
            return self.model.objects.prefetch_related(*self.request.data.get('include', [])).filter(
                **filter_fields).order_by(*order_by)

    def search(self, request, *args, **kwargs):
        """ Функция поиска объектов """
        try:
            queryset = self.get_queryset().distinct()

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(
                    page,
                    many=True,
                    context={'include': self.request.data.get('include', [])}
                )
                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(queryset, many=True,
                                               context={'include': self.request.data.get('include', [])})
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        except (exceptions.FieldError, AttributeError) as ex:
            return Response(data={
                'error': 'Переданы некорректные поля, проверьте тело запроса.',
                'msg': str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)

        except BadSearch as ex:
            return Response(data=ex.args[0], status=status.HTTP_400_BAD_REQUEST)

    def search_one(self, request, *args, **kwargs):
        """ Функция поиска объектов """
        try:
            obj = self.get_queryset().distinct().first()
        except exceptions.FieldError as ex:
            return Response(data={
                'error': 'Переданы некорректные поля, проверьте тело запроса.',
                'msg': str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)
        if obj is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj,
                                           context={'include': self.request.data.get('include', [])})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
