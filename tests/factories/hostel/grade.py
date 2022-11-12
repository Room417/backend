import pytest
import factory

from hostel_api.models import Grade


@pytest.fixture
def grade_factory():
    class GradeFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Grade

        name = factory.Sequence(lambda i: f'grade {i}')

    return GradeFactory
