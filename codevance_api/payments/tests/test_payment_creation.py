import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from codevance_api.payments.models import Supplier, Payment
from datetime import date, timedelta

from codevance_api.payments.serializers import PaymentSerializer


@pytest.fixture
def auth_operator_01(db):
    """
    Creates and returns an authenticated operator.
    """
    User = get_user_model()
    operator = User.objects.create(email='operator_01@email.com', is_operator=True)
    client = APIClient()
    client.force_authenticate(user=operator)
    return client


@pytest.fixture
def supplier_01(db):
    """
    Creates and returns a supplier.
    """
    User = get_user_model()
    user = User.objects.create(email='supplier_01@email.com')
    supplier = Supplier.objects.create(user=user)
    return supplier


@pytest.fixture
def resp_payment_creation_auth_operator_01(auth_operator_01, supplier_01):
    """
    Creates a payment and returns a response.
    """
    due_date = date.today() + timedelta(days=10)
    data = {'supplier': supplier_01.pk, 'due_date': due_date, 'value': 1000, 'creation_date': date.today()}
    resp = auth_operator_01.post('/api/payments/', data=data)
    return resp


def test_resp_payment_creation_status_code(resp_payment_creation_auth_operator_01):
    """
    Certifies that the response has a 201 status code.
    """
    assert resp_payment_creation_auth_operator_01.status_code == HTTP_201_CREATED


def test_payment_returned_in_response(resp_payment_creation_auth_operator_01, supplier_01):
    """
    Certifies the payment is returned as expected after created.
    """
    payment = Payment.objects.filter(supplier=supplier_01).first()
    serializer = PaymentSerializer(payment)
    payment_data = {'supplier': serializer.data['supplier'],
                    'creation_date': serializer.data['creation_date'],
                    'due_date': serializer.data['due_date'],
                    'value': serializer.data['value']}
    assert resp_payment_creation_auth_operator_01.data == payment_data


def test_unauth_users_can_not_create_payments(supplier_01):
    """
    Certifies that an unauthenticated user can not
    create payments.
    """
    unauth_client = APIClient()
    due_date = date.today() + timedelta(days=10)
    data = {'supplier': supplier_01.pk, 'due_date': due_date, 'value': 1000, 'creation_date': date.today()}
    resp = unauth_client.post('/api/payments/', data=data)
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_bad_request_cases(auth_operator_01, supplier_01):
    """
    Certifies that a response with 400 status code
    is returned if invalid values are filled.
    """
    due_date = date.today() + timedelta(days=10)
    invalid_due_date = date.today() - timedelta(days=1)
    # without supplier
    data_01 = {'due_date': due_date, 'value': 1000, 'creation_date': date.today()}
    # Invalid supplier ID
    data_02 = {'supplier': 12345, 'due_date': due_date, 'value': 1000, 'creation_date': date.today()}
    # Negative value
    data_03 = {'supplier': supplier_01.pk, 'due_date': due_date, 'value': -10, 'creation_date': date.today()}
    # due_date before day of creation
    data_04 = {'supplier': supplier_01.pk, 'due_date': invalid_due_date,
               'value': 1000, 'creation_date': date.today()}

    resp_01 = auth_operator_01.post('/api/payments/', data=data_01)
    resp_02 = auth_operator_01.post('/api/payments/', data=data_02)
    resp_03 = auth_operator_01.post('/api/payments/', data=data_03)
    resp_04 = auth_operator_01.post('/api/payments/', data=data_04)

    assert resp_01.status_code == HTTP_400_BAD_REQUEST
    assert resp_02.status_code == HTTP_400_BAD_REQUEST
    assert resp_03.status_code == HTTP_400_BAD_REQUEST
    assert resp_04.status_code == HTTP_400_BAD_REQUEST
