import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK
from django.contrib.auth import get_user_model


@pytest.fixture
def operator(db):
    """
    Creates and returns an operator with
    known credentials.
    """
    User = get_user_model()
    operator = User.objects.create_user(email='operator@email.com', password='operatorpass', is_operator=True)
    return operator


@pytest.fixture
def resp_token_creation(operator):
    """
    Certifies a token is created and returned when requested.
    The response should contain a dict with the keys 'refresh'
    and 'access'.
    """
    client = APIClient()
    data = {'email': 'operator@email.com', 'password': 'operatorpass'}
    resp = client.post('/api/token/', data=data)
    return resp


def test_token_created_returned_in_response(resp_token_creation):
    """
    Cretifies that the token returned in the response.
    """
    assert list(resp_token_creation.data.keys()) == ['refresh', 'access']


def test_token_refresh(resp_token_creation):
    """
    Certifies that a new token is returned when
    a request to refresh it is made.
    """
    old_access = resp_token_creation.data['access']
    data = {'refresh': resp_token_creation.data['refresh']}
    client = APIClient()
    resp = client.post('/api/token/refresh/', data=data)
    new_access = resp.data['access']
    assert 'access' in resp.data
    assert new_access != old_access


def test_token_created_works(resp_token_creation):
    """
    Certifies that the new token works to
    authenticate a request.
    """
    client = APIClient()
    token = resp_token_creation.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    resp = client.get('/api/payments/')
    assert resp.status_code == HTTP_200_OK
