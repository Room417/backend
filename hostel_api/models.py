from django.contrib.auth.models import User
from django.db import models
from .path_utils import get_photo_path, get_contract_path, get_registration_path


class Staff(models.Model):
    """Модель работника общежития"""
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    surname = models.CharField(verbose_name='Фамилия', max_length=25)
    name = models.CharField(verbose_name='Имя', max_length=25)
    patronymic = models.CharField(verbose_name='Отчество', max_length=25)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Building(models.Model):
    """Модель корпуса"""
    number = models.PositiveIntegerField(verbose_name='Номер корпуса=')
    staff = models.ManyToManyField(Staff, verbose_name='Комендант', related_name='buildings')

    def __str__(self):
        return f'Корпус №{self.number}'

    @property
    def address(self):
        """Свойство для получения адреса корпуса"""
        return f'г. Зеленоград, ул. Юности, д. {self.number}'


class Room(models.Model):
    """Модель комнаты"""
    number = models.PositiveIntegerField(verbose_name='Номер комнаты')
    building = models.ForeignKey(Building, verbose_name='Корпус', related_name='rooms', on_delete=models.CASCADE)
    max_residents = models.PositiveIntegerField(verbose_name='Максимальное число жильцов')

    def __str__(self):
        return f'{self.building.number-self.number}'

    @property
    def floor(self):
        """Свойство для получения номера этажа"""
        return self.number % 100


class Student(models.Model):
    """Модель студента"""
    surname = models.CharField(verbose_name='Фамилия', max_length=25)
    name = models.CharField(verbose_name='Имя', max_length=25)
    patronymic = models.CharField(verbose_name='Отчество', max_length=25)
    group = models.CharField(verbose_name='Группа', max_length=10)
    study_direction = models.CharField(verbose_name='Направление подготовки', max_length=50)
    student_card = models.PositiveIntegerField(verbose_name='Номер студенческого')
    auth_token = models.CharField(verbose_name='Токен аутентификации', max_length=100)
    pass_hash = models.CharField(verbose_name='Хэш пароля', max_length=256)

    def update_profile(self):
        """Функция для получения актуальной информации в начале учебного года из ОРИОКС'а"""
        pass

    def __str__(self):
        return f'{self.surname} {self.name} {self.group}'


class Grade(models.Model):
    """Модель ступени обучения"""
    name = models.CharField(verbose_name='Название', max_length=20)

    def __str__(self):
        return self.name


class Resident(models.Model):
    """Модель проживающего"""
    student = models.OneToOneField(Student, verbose_name='Студент', on_delete=models.CASCADE, related_name='resident')
    grade = models.ForeignKey(Grade, verbose_name='Ступень обучения', on_delete=models.PROTECT)
    photo = models.ImageField(verbose_name='Фото', upload_to=get_photo_path)
    birth_date = models.DateField(verbose_name='Дата рождения')
    enter_date = models.DateField(verbose_name='Дата зачисления')
    room = models.ForeignKey(Room, verbose_name='Комната', on_delete=models.PROTECT)
    contract = models.FileField(verbose_name='Договор', upload_to=get_contract_path)
    registration = models.FileField(verbose_name='Временная регистрация', upload_to=get_registration_path)

    @property
    def address(self):
        return f'{self.room.building.address}, к. {self.room.number}'

    def __str__(self):
        return self.student.__str__()
