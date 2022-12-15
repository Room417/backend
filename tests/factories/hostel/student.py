from datetime import date

import pytest
import factory
import factory.fuzzy

from hostel_api.models import Student


@pytest.fixture
def student_factory(user_factory):
    class StudentFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Student

        user = factory.SubFactory(user_factory)
        surname = factory.Sequence(lambda i: f'surname{i}')
        name = factory.Sequence(lambda i: f'name{i}')
        patronymic = factory.Sequence(lambda i: f'patronymic{i}')
        grade = Student.Grade.BACHELOR
        group = factory.Sequence(lambda i: f'group{i}')
        study_direction = factory.Sequence(lambda i: f'study_direction{i}')
        student_card = factory.Sequence(lambda i: i)

        birth_date = factory.fuzzy.FuzzyDate(date(1990, 1, 1), date(2022, 1, 1))
        enter_date = factory.fuzzy.FuzzyDate(date(1990, 1, 1), date(2022, 1, 1))

    return StudentFactory
