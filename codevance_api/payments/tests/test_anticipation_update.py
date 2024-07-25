from datetime import date
from unittest import mock

import pytest

from codevance_api.payments.models import Anticipation, RequestLog
from codevance_api.payments.payments import calc_new_value
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient


@pytest.fixture
def anticipation_payment_supp_01(payment_supplier_01):
    """
    Creates and returns an anticipation.
    """
    new_due_date = date.today()
    new_value = calc_new_value(payment_supplier_01.pk, new_due_date.isoformat())
    anticipation = Anticipation.objects.create(payment=payment_supplier_01,
                                               new_due_date=new_due_date,
                                               new_value=new_value)
    return anticipation


@pytest.fixture
def resp_update_anticip_auth_operator_01(auth_operator_01,
                                         anticipation_payment_supp_01):
    """
    Creates a request updating an anticipation and
    returns a response.
    """
    data = {'status': 'A'}
    resp = auth_operator_01.patch(f'/api/anticipations/{anticipation_payment_supp_01.pk}/', data=data)
    return resp


def test_resp_update_anticipation_status_code(resp_update_anticip_auth_operator_01):
    """
    Certifies that the response returned with a 200 status code.
    """
    assert resp_update_anticip_auth_operator_01.status_code == HTTP_200_OK


def test_anticipation_modified(resp_update_anticip_auth_operator_01,
                               anticipation_payment_supp_01):
    """
    Certifies that the anticipation was modified.
    """
    anticipation = Anticipation.objects.get(id=anticipation_payment_supp_01.pk)
    assert anticipation.status == 'A'


def test_supplier_01_can_not_update_antic_from_supp_02(auth_supplier_01, payment_supplier_02, auth_operator_01):
    """
    Certifies that a supplier can not update anticipations from others.
    """
    new_due_date = date.today()
    new_value = calc_new_value(payment_supplier_02.pk, new_due_date.isoformat())
    anticipation_02 = Anticipation.objects.create(payment=payment_supplier_02,
                                                  new_due_date=new_due_date,
                                                  new_value=new_value)
    data = {'status': 'A'}
    resp_supplier = auth_supplier_01.patch(f'/api/anticipations/{anticipation_02.pk}/', data=data)
    assert resp_supplier.status_code == HTTP_404_NOT_FOUND


def test_status_not_different_than_a_or_d(auth_operator_01, anticipation_payment_supp_01):
    """
    Certifies that an anticipation can not be updated to
    a status different from A (Approved) or D (Denied).
    """
    data = {'status': 'E'}  # wrong status
    resp = auth_operator_01.patch(f'/api/anticipations/{anticipation_payment_supp_01.pk}/', data=data)
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_unauthenticated_users_can_not_update_anticip(anticipation_payment_supp_01):
    """
    Certifies that an unauthenticated user can not update anticipations.
    """
    client = APIClient()
    data = {'status': 'A'}
    resp = client.patch(f'/api/anticipations/{anticipation_payment_supp_01.pk}/', data=data)
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_new_value_not_changed_if_tried(anticipation_payment_supp_01, auth_operator_01):
    """
    Certifies that the new_value is not changed if tried.
    """
    new_value_before_request = anticipation_payment_supp_01.new_value
    data = {'status': 'A', 'new_value': 25}  # Trying to update new_value to 25
    auth_operator_01.patch(f'/api/anticipations/{anticipation_payment_supp_01.pk}/', data=data)
    anticipation = Anticipation.objects.get(id=anticipation_payment_supp_01.pk)
    assert anticipation.status == 'A'
    assert anticipation.new_value == new_value_before_request  # new_value was kept the same


def test_common_user_requests_not_allowed(auth_common_user, anticipation_payment_supp_01):
    """
    Certifies that users that are neither suppliers
    nor operators can not list payments.
    """
    data = {'status': 'A'}
    resp = auth_common_user.patch(f'/api/anticipations/{anticipation_payment_supp_01.pk}/', data=data)
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_log_created_after_updating_an_anticipation(
        resp_update_anticip_auth_operator_01,
        anticipation_payment_supp_01):
    """
    Certifies a RequestLog is created when updating an anticipation.
    """
    assert RequestLog.objects.filter(anticipation=anticipation_payment_supp_01, action='A').exists()


@mock.patch('codevance_api.payments.payments.send_email.delay_on_commit')
def test_email_sent_after_updating_anticipations(mock_send_email,
                                                 auth_operator_01,
                                                 anticipation_payment_supp_01):
    """
    Certifies an email is sent when an anticipation is updated.
    """
    data = {'status': 'A'}
    auth_operator_01.patch(f'/api/anticipations/{anticipation_payment_supp_01.pk}/', data=data)
    mock_send_email.assert_called_once_with(sub='A',
                                            recipient=[f'{anticipation_payment_supp_01.payment.supplier.user.email}'],
                                            ant_id=anticipation_payment_supp_01.pk)
