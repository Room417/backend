import pytest
import factory

from hostel_api.models import Resident


@pytest.fixture
def resident_factory(student_factory, room_factory):
    class ResidentFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Resident

        student = factory.SubFactory(student_factory)
        room = factory.SubFactory(room_factory)

    return ResidentFactory
