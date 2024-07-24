import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from codevance_api.payments.models import Payment
from datetime import date, timedelta

from codevance_api.payments.serializers import PaymentSerializer


@pytest.fixture
def resp_payment_creation_auth_operator_01(auth_operator_01, supplier_01):
    """
    Creates a payment and returns a response.
    """
    due_date = date.today() + timedelta(days=10)
    data = {'supplier': supplier_01.pk, 'due_date': due_date, 'value': 1000}
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
    data = {'supplier': supplier_01.pk, 'due_date': due_date, 'value': 1000}
    resp = unauth_client.post('/api/payments/', data=data)
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_bad_request_cases(auth_operator_01, auth_supplier_01, supplier_01, supplier_02):
    """
    Certifies that a response with 400 status code
    is returned if invalid values are filled.
    """
    due_date = date.today() + timedelta(days=10)
    invalid_due_date = date.today() - timedelta(days=1)

    data_01 = {'due_date': due_date, 'value': 1000}  # without supplier
    data_02 = {'due_date': due_date, 'value': 1000}  # Invalid supplier ID
    data_03 = {'supplier': supplier_01.pk, 'due_date': due_date, 'value': -10}  # Negative value
    data_04 = {'supplier': supplier_01.pk, 'due_date': invalid_due_date, 'value': 1000}  # invalid due_date

    resp_01 = auth_operator_01.post('/api/payments/', data=data_01)
    resp_02 = auth_operator_01.post('/api/payments/', data=data_02)
    resp_03 = auth_operator_01.post('/api/payments/', data=data_03)
    resp_04 = auth_operator_01.post('/api/payments/', data=data_04)

    assert resp_01.status_code == HTTP_400_BAD_REQUEST
    assert resp_02.status_code == HTTP_400_BAD_REQUEST
    assert resp_03.status_code == HTTP_400_BAD_REQUEST
    assert resp_04.status_code == HTTP_400_BAD_REQUEST


def test_payment_created_correctly_with_wrong_supplier_id(auth_supplier_01, supplier_02, supplier_01):
    """
    Certifies that, even if a supplier inform the wrong ID when
    creating a payment, the payment is created correctly (related
    to him and not to others).
    """
    due_date = date.today() + timedelta(days=10)
    data = {'supplier': supplier_02.pk, 'due_date': due_date, 'value': 1122.33}  # invalid supplier's ID
    resp = auth_supplier_01.post('/api/payments/', data=data)

    assert resp.status_code == HTTP_201_CREATED
    assert Payment.objects.filter(value=1122.33).filter(supplier=supplier_01).exists()
    assert not Payment.objects.filter(value=1122.33).filter(supplier=supplier_02).exists()


def test_payment_created_if_supplier_do_not_inform_his_id(auth_supplier_01):
    """
    If a supplier tries to create a payment without informing
    his ID, he has to be identified automatically.
    """
    due_date = date.today() + timedelta(days=10)
    data = {'due_date': due_date, 'value': 1245.35}
    resp = auth_supplier_01.post('/api/payments/', data=data)

    assert resp.status_code == HTTP_201_CREATED
    assert Payment.objects.filter(value=1245.35).exists()
