import pytest


#from rest_framework.test import APIClient


@pytest.fixture
def get_auth_client(client):
    def _get_auth_client(user):
        client.force_login(user=user)
        return client

    return _get_auth_client

# @pytest.fixture
# def auth_client_user(user):
#     client = APIClient()
#     client.force_authenticate(user=user)
#     return client