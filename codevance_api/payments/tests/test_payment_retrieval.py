import pytest
from rest_framework.status import (HTTP_200_OK, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED)
from rest_framework.test import APIClient

from codevance_api.payments.serializers import PaymentSerializer


@pytest.fixture
def resp_retrieve_payment_auth_operator_01(auth_operator_01,
                                           payment_supplier_01):
    """
    Creates a request retrieving a payment and returns a response.
    """
    resp = auth_operator_01.get(f'/api/payments/{payment_supplier_01.pk}/')
    return resp


def test_status_code_retrieve_payment(resp_retrieve_payment_auth_operator_01):
    """
    Certifies that a 200 status code response was returned.
    """
    assert resp_retrieve_payment_auth_operator_01.status_code == HTTP_200_OK


def test_payment_returned_in_the_response(resp_retrieve_payment_auth_operator_01,
                                          payment_supplier_01):
    """
    Certifies that the payment returned as expected in the response.
    """
    serializer = PaymentSerializer(payment_supplier_01)
    payment_data = {'id': serializer.data['id'],
                    'supplier': serializer.data['supplier'],
                    'creation_date': serializer.data['creation_date'],
                    'due_date': serializer.data['due_date'],
                    'value': serializer.data['value']}
    assert resp_retrieve_payment_auth_operator_01.data == payment_data


def test_unauthenticated_users_can_not_retrieve_payments(payment_supplier_01):
    """
    Certifies that an unauthenticated user can not retrieve a payment.
    """
    client = APIClient()
    resp = client.get(f'/api/payments/{payment_supplier_01.pk}/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_common_users_can_not_retrieve_payments(auth_common_user,
                                                payment_supplier_01):
    """
    Certifies that a user who is neither an operator nor
    a supplier can not retrieve payments.
    """
    resp = auth_common_user.get(f'/api/payments/{payment_supplier_01.pk}/')
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_supplier_01_can_not_retrieve_payments_from_other(auth_supplier_01,
                                                          payment_supplier_02):
    """
    Certifies that a supplier can not retrieve other supplier's payments.
    """
    resp = auth_supplier_01.get(f'/api/payments/{payment_supplier_02.pk}/')
    assert resp.status_code == HTTP_404_NOT_FOUND
