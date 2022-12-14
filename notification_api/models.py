from django.db import models
from datetime import date


from hostel_api.models import Staff, Resident


class Notification(models.Model):
    """ Модель уведомления """
    author = models.ForeignKey(Staff, verbose_name='Автор', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=50)
    description = models.TextField(verbose_name='Описание', max_length=1000)
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    recipients = models.ManyToManyField(Resident, verbose_name='Получатели', related_name='notifications')
    start_date = models.DateField(verbose_name='Дата начала отображения')
    end_date = models.DateField(verbose_name='Дата конца отображения')

    def __str__(self):
        return f'{self.title}. Автор: {self.author.__str__()}'

    @property
    def is_active(self) -> bool:
        return self.start_date <= date.today() <= self.end_date


class Request(models.Model):
    """ Модель заявки """
    author = models.ForeignKey(Resident, verbose_name='Автор', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Staff, verbose_name='Получатель', related_name='requests')
    title = models.CharField(verbose_name='Заголовок', max_length=50)
    description = models.TextField(verbose_name='Описание', max_length=1000)
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_seen = models.BooleanField(verbose_name='Просмотрено', default=False)
    archived = models.BooleanField(verbose_name='Заархивировано', default=False)
    is_provided = models.BooleanField(verbose_name='Услуга оказана', default=False)
    provision_date = models.DateField(verbose_name='Дата оказания услуги', null=True)

    def __str__(self):
        return f'{self.title}. Автор: {self.author.__str__()}'
