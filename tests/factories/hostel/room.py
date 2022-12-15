import pytest
import factory
import factory.fuzzy

from hostel_api.models import Room


@pytest.fixture
def room_factory(building_factory):
    class RoomFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Room

        number = factory.Sequence(lambda i: i)
        building = factory.SubFactory(building_factory)
        max_residents = factory.fuzzy.FuzzyInteger(2, 4)

    return RoomFactory
