import pytest

pytest_plugins = [
    'tests.factories.hostel.client',
    'tests.factories.hostel.staff',
    'tests.factories.hostel.student',
    'tests.factories.hostel.building',
    'tests.factories.hostel.room',
    'tests.factories.hostel.grade',
    'tests.factories.hostel.resident',
]
