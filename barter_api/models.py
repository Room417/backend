from django.db import models
from hostel_api.models import Student


class Product(models.Model):
    """Модель товара"""
    author = models.ForeignKey(Student, verbose_name='Автор объявления', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=50)
    description = models.TextField(verbose_name='Описание', max_length=1000)
    price = models.PositiveIntegerField(verbose_name='Цена', null=True)
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)

    def __str__(self):
        return f'{self.title} ({self.author.surname})'
