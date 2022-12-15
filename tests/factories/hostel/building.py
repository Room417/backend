import pytest
import factory

from hostel_api.models import Building


@pytest.fixture
def building_factory():
    class BuildingFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Building

        number = factory.Sequence(lambda i: i)

        @factory.post_generation
        def staff(self, create, extracted, **kwargs):
            if not create:
                return

            if extracted:
                for group in extracted:
                    self.staff.add(group)

    return BuildingFactory
