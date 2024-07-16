import pytest
from werkzeug.security import generate_password_hash
from peewee import SqliteDatabase
from flask import session

from app import app
from projects.auth.models import User, Departments


class TestUser:

    @classmethod
    def name_class(cls):
        return cls.__name__

    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    @pytest.fixture(scope='class')
    def test_db(self):
        name_class = self.name_class()
        filename = f'test_{name_class}.sqlite'
        _db = SqliteDatabase(filename)
        models = [User, Departments]
        _db.bind(models)
        _db.create_tables(models)

        user_email = 'test@test.ru'
        user_password_hash = generate_password_hash('12345678q')
        user_dep = Departments.create(department='ПТО')

        User.create(
            name='Петя',
            surname='Петров',
            email=user_email,
            password=user_password_hash,
            department=user_dep
        )
        yield _db
        _db.drop_tables(models)

    def test_login_valid(self, client, test_db):
        data = {
            'email': 'test@test.ru',
            'password': '12345678q',
        }
        response = client.post('auth/login', data=data)
        assert response.status_code == 302

    def test_login_invalid(self, client, test_db):
        data = {
            'email': 't@t.ru',
            'password': '123',
        }
        response = client.post('auth/login', data=data)
        assert response.status_code == 200

    def test_input_personal_data_invalid(self, client, test_db):
        data = {
            'user_name': 'Ким',
            'user_surname': 'Ким',
            'user_email': 'dd@asf.rываыфu',  # Ошибка
            'user_password': '13245678kim',
            'user_select_department': 'Руководство',
        }
        response = client.post('auth/registrate_personal_account', data=data)
        assert response.status_code == 200  # Проверяем, что запрос остается на той же странице

    def test_input_personal_data_valid(self, client, test_db):
        data = {
            'user_name': 'Опасный',
            'user_surname': 'Парень',
            'user_email': 'test4test@test4test.ru',
            'user_password': '12345678dfg',
            'user_select_department': 'ПТО',
        }
        response = client.post('auth/registrate_personal_account', data=data)
        assert response.status_code == 302  # Проверяем редирект на страницу успешной регистрации
