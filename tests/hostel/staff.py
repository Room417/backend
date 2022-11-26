import pytest
from django.urls import reverse


@pytest.fixture()
def initial_data(db, staff_factory, building_factory):
    # создаем работников общежития
    staff1 = staff_factory(surname='Иванов', name='Иван', patronymic='Иванович')
    staff_factory(surname='Иванов', name='Александр', patronymic='Иванович')
    staff3 = staff_factory(surname='Александров', name='Петр', patronymic='Александрович')

    # создаем корпуса
    building1 = building_factory(staff=[staff1, staff3])

    building2 = building_factory(staff=[staff1])

    return {
        'building1': building1,
        'building2': building2
    }


@pytest.mark.parametrize('filters', [{}, {'surname': 'Иванов'}, {'surname': 'Иванов', 'name': 'Александр'}])
def test_filter_staff(client, initial_data, filters):
    data = {
        'filter': filters
    }
    response = client.post(reverse('persons-staff-custom-search'), data=data, content_type='application/json')
    assert response.status_code == 200
    persons = response.json()
    if filters == {}:
        assert len(persons) == 3

    elif filters == {'surname': 'Иванов'}:
        assert len(persons) == 2
        assert persons[0]['surname'] == 'Иванов'
        assert persons[1]['surname'] == 'Иванов'

    else:
        assert len(persons) == 1
        assert persons[0]['surname'] == 'Иванов'
        assert persons[0]['name'] == 'Александр'


@pytest.mark.parametrize('sort', [[], ['-surname', 'name'], ['name']])
def test_sort_staff(client, initial_data, sort):
    data = {
        'sort': sort
    }
    response = client.post(reverse('persons-staff-custom-search'), data=data, content_type='application/json')
    assert response.status_code == 200
    persons = response.json()
    assert len(persons) == 3
    if sort == ['name']:
        assert persons[0]['name'] == 'Александр'
        assert persons[1]['name'] == 'Иван'
        assert persons[2]['name'] == 'Петр'
    elif sort == ['-surname', 'name']:
        assert persons[0]['surname'] == 'Иванов'
        assert persons[0]['name'] == 'Александр'
        assert persons[1]['surname'] == 'Иванов'
        assert persons[1]['name'] == 'Иван'
        assert persons[2]['surname'] == 'Александров'
    else:
        assert persons[0]['surname'] == 'Александров'
        assert persons[1]['surname'] == 'Иванов'
        assert persons[1]['name'] == 'Александр'
        assert persons[2]['surname'] == 'Иванов'
        assert persons[2]['name'] == 'Иван'


@pytest.mark.parametrize('include', [[], ['buildings']])
def test_include_staff(client, initial_data, include):
    data = {
        'include': include
    }
    response = client.post(reverse('persons-staff-custom-search'), data=data, content_type='application/json')
    assert response.status_code == 200
    persons = response.json()
    assert len(persons) == 3
    if include:
        assert persons[0]['buildings'] == [{
            'number': initial_data['building1'].number,
            'address': initial_data['building1'].address
        }]
        assert persons[1]['buildings'] == []
        assert persons[2]['buildings'] == [
            {
                'number': initial_data['building1'].number,
                'address': initial_data['building1'].address
            },
            {
                'number': initial_data['building2'].number,
                'address': initial_data['building2'].address
            }
        ]

    else:
        assert persons[0]['buildings'] == [initial_data['building1'].number]
        assert persons[1]['buildings'] == []
        assert persons[2]['buildings'] == [initial_data['building1'].number, initial_data['building2'].number]
