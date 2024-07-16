import pytest
from werkzeug.security import generate_password_hash
from peewee import SqliteDatabase
from app import app
from projects.auth.models import User, Departments


class TestAccessPersonalCabinetPage:

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
        user_password_hash = generate_password_hash('123')
        user_dep = Departments.create(department='ПТО')

        User.create(
            name='Петя',
            surname='Петров',
            email=user_email,
            password=user_password_hash,
            department=user_dep,
        )
        yield _db
        _db.drop_tables(models)

    @pytest.fixture
    def logged_in_client(self, client):
        with client.session_transaction() as s:
            s['userLogged'] = 'test@test.ru'
        return client

    def test_login_valid(self, client, test_db):
        data = {
            'email': 'test@test.ru',
            'password': '123',
        }
        response = client.post('auth/login', data=data)
        assert response.status_code == 302

    def test_personal_cabinet_page(self, logged_in_client):
        response = logged_in_client.get('personal_cabinet/')
        assert response.status_code == 200

    def test_analysis_effectiveness_projects_page(self, logged_in_client):
        response = logged_in_client.get('analysis_effectiveness_projects/')
        assert response.status_code == 200

    def test_bank_page(self, logged_in_client):
        response = logged_in_client.get('bank/')
        assert response.status_code == 200

    def test_expenses_and_income_page(self, logged_in_client):
        response = logged_in_client.get('expenses_income/')
        assert response.status_code == 200

    def test_finance_receipts_page(self, logged_in_client):
        response = logged_in_client.get('finance_receipts/')
        assert response.status_code == 200

    def test_financial_statements_page(self, logged_in_client):
        response = logged_in_client.get('financial_statements/')
        assert response.status_code == 200

    def test_expenses_income_page(self, logged_in_client):
        response = logged_in_client.get('expenses_income/')
        assert response.status_code == 200

    def test_withdrawals_page(self, logged_in_client):
        response = logged_in_client.get('withdrawals/')
        assert response.status_code == 200
