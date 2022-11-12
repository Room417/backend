import pytest
from django.urls import reverse


@pytest.fixture()
def initial_data(db, student_factory):
    # создаем студентов
    student_factory(surname='Иванов', name='Иван', patronymic='Иванович')
    student_factory(surname='Иванов', name='Александр', patronymic='Иванович')
    student_factory(surname='Александров', name='Петр', patronymic='Александрович')


@pytest.mark.parametrize('filters', [{}, {'surname': 'Иванов'}, {'surname': 'Иванов', 'name': 'Александр'}])
def test_filter_student(client, initial_data, filters):
    data = {
        'filter': filters
    }
    response = client.post(reverse('persons-students-search'), data=data, content_type='application/json')
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
def test_sort_student(client, initial_data, sort):
    data = {
        'sort': sort
    }
    response = client.post(reverse('persons-students-search'), data=data, content_type='application/json')
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


@pytest.mark.parametrize('correct', [True, False])
def test_get_one_student(client, initial_data, correct):
    if correct:
        data = {
            'filter': {
                'surname': 'Иванов',
                'name': 'Иван'
            }
        }
    else:
        data = {
            'filter': {
                'surname': 'Абракадабра',
                'name': 'Абракадабра'
            }
        }
    response = client.post(reverse('persons-students-search-one'), data=data, content_type='application/json')

    if correct:
        person = response.json()
        assert response.status_code == 200
        assert person['surname'] == 'Иванов'
        assert person['name'] == 'Иван'

    else:
        assert response.status_code == 404
