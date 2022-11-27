import pytest
from django.urls import reverse


@pytest.fixture()
def initial_data(db, student_factory, resident_factory, building_factory, room_factory):
    # создаем студентов
    student1 = student_factory(surname='Иванов', name='Иван', patronymic='Иванович')
    student2 = student_factory(surname='Иванов', name='Александр', patronymic='Иванович')
    student3 = student_factory(surname='Александров', name='Петр', patronymic='Александрович')

    # создаем корпус и комнату
    building = building_factory(number=11)
    room = room_factory(building=building, number=15)

    # заселяем студентов
    resident_factory(student=student1, room=room)
    resident_factory(student=student2, room=room)
    resident_factory(student=student3, room=room)


@pytest.mark.parametrize('filters', [
    {},
    {'student__surname': 'Иванов'},
    {'student__surname': 'Иванов', 'student__name': 'Александр'},
    {'room__building__number': 11},
    {'room__number': 15}
])
def test_filter_resident(initial_data, client, filters):
    data = {
        'filter': filters,
        'include': ['student']
    }
    response = client.post(reverse('persons-residents-search'), data=data, content_type='application/json')
    assert response.status_code == 200
    persons = response.json()['data']
    if filters == {} or filters == {'room__building__number': 11} or filters == {'room__number': 15}:
        assert len(persons) == 3

    elif filters == {'student__surname': 'Иванов'}:
        assert len(persons) == 2

    else:
        assert len(persons) == 1
        assert persons[0]['student']['surname'] == 'Иванов'
        assert persons[0]['student']['name'] == 'Александр'


@pytest.mark.parametrize('sort', [[], ['-student__surname', 'student__name'], ['student__name']])
def test_sort_resident(client, initial_data, sort):
    data = {
        'sort': sort,
        'include': ['student']
    }
    response = client.post(reverse('persons-residents-search'), data=data, content_type='application/json')
    assert response.status_code == 200
    persons = response.json()['data']
    assert len(persons) == 3
    if sort == ['student__name']:
        assert persons[0]['student']['name'] == 'Александр'
        assert persons[1]['student']['name'] == 'Иван'
        assert persons[2]['student']['name'] == 'Петр'
    elif sort == ['-student__surname', 'student__name']:
        assert persons[0]['student']['surname'] == 'Иванов'
        assert persons[0]['student']['name'] == 'Александр'
        assert persons[1]['student']['surname'] == 'Иванов'
        assert persons[1]['student']['name'] == 'Иван'
        assert persons[2]['student']['surname'] == 'Александров'
    else:
        assert persons[0]['student']['surname'] == 'Александров'
        assert persons[1]['student']['surname'] == 'Иванов'
        assert persons[1]['student']['name'] == 'Александр'
        assert persons[2]['student']['surname'] == 'Иванов'
        assert persons[2]['student']['name'] == 'Иван'


@pytest.mark.parametrize('correct', [True, False])
def test_get_one_resident(client, initial_data, correct):
    if correct:
        data = {
            'filter': {
                'student__surname': 'Иванов',
                'student__name': 'Иван'
            },
            'include': ['student']
        }
    else:
        data = {
            'filter': {
                'student__surname': 'Абракадабра',
                'student__name': 'Абракадабра'
            }
        }
    response = client.post(reverse('persons-residents-search-one'), data=data, content_type='application/json')

    if correct:
        person = response.json()
        assert response.status_code == 200
        assert person['student']['surname'] == 'Иванов'
        assert person['student']['name'] == 'Иван'

    else:
        assert response.status_code == 404


@pytest.mark.parametrize('is_full', [True, False])
def test_relocate(db, client, is_full, student_factory, room_factory, building_factory, resident_factory):
    # создаем корпус и комнаты
    building = building_factory(number=11)
    room1 = room_factory(building=building, number=15)
    room2 = room_factory(building=building, number=16, max_residents=1)

    # заселяем студентов
    resident = resident_factory(room=room1)

    if is_full:
        resident_factory(room=room2)

    response = client.post(
        reverse('persons-residents-relocate'),
        data={'room_id': room2.id, 'resident_id': resident.id},
        content_type='application/json'
    )

    if is_full:
        assert response.status_code == 400
        assert response.json() == {
                'error': 'Переселение невозможно',
                'msg': 'Комната заполнена. Переселение невозможно'
            }

    else:
        assert response.status_code == 200
        resident.refresh_from_db()
        assert resident.room == room2


@pytest.mark.parametrize('data', [
    {},
    {'room_id': 1},
    {'room_id': 'room_id'},
    {'resident_id': 'resident_id'},
    {'resident_id': 1}
])
def test_incorrect_request_body_relocate(client, data):
    response = client.post(reverse('persons-residents-relocate'), data=data, content_type='application/json')
    assert response.status_code == 400


@pytest.mark.parametrize('error', ['resident', 'room'])
def test_nonexistent_room_or_resident(db, client, room_factory, resident_factory, error):
    if error == 'resident':
        room = room_factory()
        data = {'room_id': room.id, 'resident_id': 0}

        expected_error = {
                'error': 'Объект не найден',
                'msg': 'Проживающего с таким id не существует'
            }

    else:
        resident = resident_factory()
        data = {'room_id': 0, 'resident_id': resident.id}

        expected_error = {
                'error': 'Объект не найден',
                'msg': 'Комнаты с таким id не существует'
            }

    response = client.post(reverse('persons-residents-relocate'), data=data, content_type='application/json')
    assert response.status_code == 400
    assert response.json() == expected_error
