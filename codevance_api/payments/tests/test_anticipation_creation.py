from datetime import date

import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from codevance_api.payments.models import Anticipation
from codevance_api.payments.serializers import AnticipationSerializer


@pytest.fixture
def resp_anticipation_creation_auth_operator_01(auth_operator_01, payment_supplier_01):
    """
    Creates an anticipation and returns a response.
    """
    new_due_date = date.today()
    data = {'payment': payment_supplier_01.pk, 'new_due_date': new_due_date}
    resp = auth_operator_01.post('/api/anticipations/', data=data)
    return resp


def test_anticipation_creation_status_code(resp_anticipation_creation_auth_operator_01):
    """
    Certifies the response returns with a 201 status code.
    """
    assert resp_anticipation_creation_auth_operator_01.status_code == HTTP_201_CREATED


def test_anticipation_returned_in_response(resp_anticipation_creation_auth_operator_01, payment_supplier_01):
    """
    Certifies that the anticipation created is returned in the response.
    """
    anticipation = Anticipation.objects.filter(payment=payment_supplier_01).first()
    serializer = AnticipationSerializer(anticipation)
    antic_data = {'payment': serializer.data['payment'],
                  'creation_date': serializer.data['creation_date'],
                  'new_due_date': serializer.data['new_due_date'],
                  'new_value': serializer.data['new_value'],
                  'update_date': serializer.data['update_date'],
                  'status': serializer.data['status']}
    assert resp_anticipation_creation_auth_operator_01.data == antic_data


def test_unauthenticated_user_can_not_create_anticipation(payment_supplier_01):
    """
    Certifies that unauthenticated users can not create anticipations.
    """
    client = APIClient()
    new_due_date = date.today()
    data = {'payment': payment_supplier_01.pk, 'new_due_date': new_due_date}
    resp = client.post('/api/anticipations/', data=data)
    assert resp.status_code == HTTP_403_FORBIDDEN
