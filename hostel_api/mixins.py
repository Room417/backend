from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.core import exceptions


class DefaultViewMixin(ModelViewSet):
    """ Миксин для реализации поиска объектов """
    model = None
    default_sort_fields = []
    default_filter_fields = {}
    default_include_fields = []

    def get_queryset(self):
        """ Получение queryset'a с заданной фильтрацией, сортировкой, включением нужных связанных объектов"""
        data = self.request.data
        order_by = data.get('sort')
        if not order_by:
            order_by = self.default_sort_fields
        filter_fields = data.get('filter', self.default_filter_fields)

        return self.model.objects.prefetch_related(*self.request.data.get('include', [])).filter(
            **filter_fields).order_by(*order_by)

    def search(self, request, *args, **kwargs):
        """ Функция поиска объектов """
        try:
            query_set = self.get_queryset().distinct()
            serializer = self.serializer_class(query_set, many=True,
                                               context={'include': self.request.data.get('include', [])})
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        except (exceptions.FieldError, AttributeError) as ex:
            return Response(data={
                'error': 'Переданы некорректные поля, проверьте тело запроса.',
                'msg': str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)

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
