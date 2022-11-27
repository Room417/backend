from datetime import date

import pytest
import factory
import factory.fuzzy

from hostel_api.models import Resident


@pytest.fixture
def resident_factory(student_factory, grade_factory, room_factory):
    class ResidentFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Resident

        student = factory.SubFactory(student_factory)
        grade = factory.SubFactory(grade_factory)
        birth_date = factory.fuzzy.FuzzyDate(date(1990, 1, 1), date(2022, 1, 1))
        enter_date = factory.fuzzy.FuzzyDate(date(1990, 1, 1), date(2022, 1, 1))
        room = factory.SubFactory(room_factory)

    return ResidentFactory
