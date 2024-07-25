import pytest

from codevance_api.payments.models import Payment
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from codevance_api.payments.serializers import PaymentSerializer


@pytest.fixture
def resp_list_payments_auth_operator_01(auth_operator_01,
                                        payment_supplier_01,
                                        payment_supplier_02):
    """
    Creates a request to list the payments and returns a response.
    """
    resp = auth_operator_01.get('/api/payments/')
    return resp


def test_status_code_list_payments(resp_list_payments_auth_operator_01):
    """
    Certifies that the response has a 200 status code.
    """
    assert resp_list_payments_auth_operator_01.status_code == HTTP_200_OK


def test_all_payments_are_present_for_operator(resp_list_payments_auth_operator_01):
    """
    Certifies that the operator can see payments from all suppliers.
    """
    payment_01 = Payment.objects.filter(supplier__corporate_name='Supplier 01').first()
    payment_02 = Payment.objects.filter(supplier__corporate_name='Supplier 02').first()
    serializer_01 = PaymentSerializer(payment_01)
    serializer_02 = PaymentSerializer(payment_02)
    assert serializer_01.data in resp_list_payments_auth_operator_01.data['results']
    assert serializer_02.data in resp_list_payments_auth_operator_01.data['results']


def test_supplier_01_can_not_see_supplier_02_payments(auth_supplier_01,
                                                      payment_supplier_01,
                                                      payment_supplier_02):
    """
    Certifies that one supplier can not see payments from others.
    """
    payment_01 = Payment.objects.get(id=payment_supplier_01.pk)
    payment_02 = Payment.objects.get(id=payment_supplier_02.pk)
    resp = auth_supplier_01.get('/api/payments/')
    serializer_01 = PaymentSerializer(payment_01)
    serializer_02 = PaymentSerializer(payment_02)
    assert serializer_01.data in resp.data['results']
    assert serializer_02.data not in resp.data['results']


def test_common_user_requests_not_allowed(auth_common_user):
    """
    Certifies that users that are neither suppliers
    nor operators can not list payments.
    """
    resp = auth_common_user.get('/api/payments/')
    assert resp.status_code == HTTP_403_FORBIDDEN
