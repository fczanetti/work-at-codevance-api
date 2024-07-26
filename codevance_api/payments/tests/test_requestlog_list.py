from datetime import date

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from codevance_api.payments.models import RequestLog
from codevance_api.payments.serializers import RequestLogSerializer


@pytest.fixture
def anticipations(auth_operator_01,
                  payment_supplier_01,
                  payment_supplier_02):
    """
    Creates some anticipations to have some
    RequestLogs registered.
    """
    new_due_date = date.today()
    data_01 = {'payment': payment_supplier_01.pk, 'new_due_date': new_due_date}
    data_02 = {'payment': payment_supplier_02.pk, 'new_due_date': new_due_date}
    auth_operator_01.post('/api/anticipations/', data=data_01)
    auth_operator_01.post('/api/anticipations/', data=data_02)
    return


@pytest.fixture
def resp_list_logs_auth_operator_01(auth_operator_01, anticipations):
    """
    Creates a request listing the RequestLogs and
    returns a response.
    """
    resp = auth_operator_01.get('/api/logs/')
    return resp


def test_request_logs_status_code(resp_list_logs_auth_operator_01):
    """
    Certifies that the response returned with a 200 status code.
    """
    assert resp_list_logs_auth_operator_01.status_code == HTTP_200_OK


def test_logs_returned_in_response(resp_list_logs_auth_operator_01):
    """
    Certifies that the logs are present in the response and
    in the expected format.
    """
    log = RequestLog.objects.first()
    serializer = RequestLogSerializer(log)
    log_data = {'id': serializer.data['id'],
                'anticipation': serializer.data['anticipation'],
                'created_at': serializer.data['created_at'],
                'user': serializer.data['user'],
                'action': serializer.data['action']}
    assert log_data in resp_list_logs_auth_operator_01.data['results']
    assert len(resp_list_logs_auth_operator_01.data['results']) == 2


def test_unauthenticated_users_can_not_request_logs(db):
    """
    Certifies that unauthenticated users can not see logs.
    """
    client = APIClient()
    resp = client.get('/api/logs/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_common_users_can_not_see_logs(auth_common_user):
    """
    Certifies that a common user can not see logs.
    """
    resp = auth_common_user.get('/api/logs/')
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_supplier_01_can_not_see_logs_from_others(anticipations,
                                                  auth_supplier_01,
                                                  supplier_01,
                                                  supplier_02):
    """
    Certifies a supplier can not see logs from other supplier.
    """
    log_01 = RequestLog.objects.get(anticipation__payment__supplier=supplier_01)
    log_02 = RequestLog.objects.get(anticipation__payment__supplier=supplier_02)
    serializer_01 = RequestLogSerializer(log_01)
    serializer_02 = RequestLogSerializer(log_02)
    resp = auth_supplier_01.get('/api/logs/')
    assert serializer_01.data in resp.data['results']
    assert serializer_02.data not in resp.data['results']
