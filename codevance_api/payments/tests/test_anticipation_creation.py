from datetime import date, timedelta
from unittest import mock

import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from codevance_api.payments.models import Anticipation, RequestLog
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
    antic_data = {'id': serializer.data['id'],
                  'payment': serializer.data['payment'],
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


def test_invalid_requests(auth_operator_01,
                          payment_supplier_01,
                          payment_supplier_02,
                          auth_supplier_01):
    """
    Certifies that invalid requests return a
    400 status code response.
    """
    new_due_date = date.today()
    invalid_date = date.today() - timedelta(days=1)
    invalid_format_date = date.today().strftime('%d/%m/%Y')

    data_01 = {'payment': payment_supplier_01.pk, 'new_due_date': invalid_date}  # invalid new_due_date
    data_02 = {'payment': payment_supplier_01.pk, 'new_due_date': invalid_format_date}  # invalid new_due_date format
    data_03 = {'payment': payment_supplier_01.pk}  # new_due_date not informed
    data_04 = {'payment': payment_supplier_02.pk, 'new_due_date': new_due_date}  # invalid payment (from other supplier)
    data_05 = {'payment': 12345, 'new_due_date': new_due_date}  # nonexistent payment_id
    data_06 = {'new_due_date': new_due_date}  # payment_id not informed

    resp_01 = auth_operator_01.post('/api/anticipations/', data=data_01)
    resp_02 = auth_operator_01.post('/api/anticipations/', data=data_02)
    resp_03 = auth_operator_01.post('/api/anticipations/', data=data_03)
    resp_04 = auth_supplier_01.post('/api/anticipations/', data=data_04)
    resp_05 = auth_supplier_01.post('/api/anticipations/', data=data_05)
    resp_06 = auth_supplier_01.post('/api/anticipations/', data=data_06)

    assert resp_01.status_code == HTTP_400_BAD_REQUEST
    assert resp_02.status_code == HTTP_400_BAD_REQUEST
    assert resp_03.status_code == HTTP_400_BAD_REQUEST
    assert resp_04.status_code == HTTP_400_BAD_REQUEST
    assert resp_05.status_code == HTTP_400_BAD_REQUEST
    assert resp_06.status_code == HTTP_400_BAD_REQUEST


def test_common_user_requests_not_allowed(auth_common_user, payment_supplier_01):
    """
    Certifies that users that are neither suppliers
    nor operators can not make requests.
    """
    new_due_date = date.today()
    data = {'payment': payment_supplier_01.pk, 'new_due_date': new_due_date}
    resp = auth_common_user.post('/api/anticipations/', data=data)
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_log_created_after_creating_anticipation(
        resp_anticipation_creation_auth_operator_01,
        payment_supplier_01):
    """
    Certifies a RequestLog is created after creating an anticipation.
    """
    anticipation = Anticipation.objects.filter(payment=payment_supplier_01).first()
    assert RequestLog.objects.filter(anticipation=anticipation, action='R').exists()


@mock.patch('codevance_api.payments.payments.send_email.delay_on_commit')
def test_email_sent_after_creating_anticipations(mock_send_email,
                                                 auth_operator_01,
                                                 payment_supplier_01):
    """
    Certifies an email is sent when an anticipation is created.
    """
    new_due_date = date.today()
    data = {'payment': payment_supplier_01.pk, 'new_due_date': new_due_date}
    auth_operator_01.post('/api/anticipations/', data=data)
    mock_send_email.assert_called_once_with(sub='new_ant',
                                            recipient=[f'{payment_supplier_01.supplier.user.email}'],
                                            ant_id=payment_supplier_01.anticipation.pk)
