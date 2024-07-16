import pytest
from app import app


class TestAccessWebSitePage:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    def test_index_page(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_invite_tender_page(self, client):
        response = client.get(
            '/invite_tender/'
        )
        assert response.status_code == 200

    def test_login_page(self, client):
        response = client.get(
            '/auth/login'
        )
        assert response.status_code == 200

    def test_contact_page(self, client):
        response = client.get(
            '/contact/'
        )
        assert response.status_code == 200

    def test_registrate_personal_account_page(self, client):
        response = client.get(
            '/auth/registrate_personal_account'
        )
        assert response.status_code == 200

    def test_password_recovery_page(self, client):
        response = client.get(
            '/auth/password_recovery'
        )
        assert response.status_code == 200

    def test_invalid_data(self, client):
        response = client.post(
            '/auth/registrate_personal_account',
            data={}
        )
        assert response.status_code == 400

    def test_unauthorized_page(self, client):
        response = client.get(
            '/personal_cabinet/'
        )
        assert response.status_code == 401

    def test_404_page(self, client):
        response = client.get(
            '/none_page/'
        )
        assert response.status_code == 404
