import factory
import pytest
from django.contrib.auth.models import User

from hostel_api.models import (
    Staff
)


@pytest.fixture
def user_factory():
    class UserFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = User

        username = factory.Sequence(lambda i: f'user{i}')

    return UserFactory


@pytest.fixture
def staff_factory(user_factory):
    class StaffFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Staff

        user = factory.SubFactory(user_factory)
        surname = factory.Sequence(lambda i: f'surname{i}')
        name = factory.Sequence(lambda i: f'name{i}')
        patronymic = factory.Sequence(lambda i: f'patronymic{i}')

    return StaffFactory
