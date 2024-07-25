from datetime import timedelta, date

import pytest

from codevance_api.payments.models import Payment, Anticipation
from codevance_api.payments.payments import calc_new_value
from codevance_api.payments.serializers import PaymentSerializer


@pytest.fixture
def payment_available_to_anticipate(db, supplier_01):
    """
    Creates a payment that is available to anticipate.
    It means there is no anticipation related and the
    due_date is greater than today.
    """
    due_date = date.today() + timedelta(days=10)
    data = {'supplier': supplier_01, 'due_date': due_date, 'value': 10}
    payment = Payment.objects.create(**data)
    return payment


@pytest.fixture
def payment_unavailable_to_anticipate(db, supplier_01):
    """
    Creates a payment that is not available to anticipate.
    It means its due_date was already reached.
    """
    due_date = date.today()
    data = {'supplier': supplier_01, 'due_date': due_date, 'value': 20}
    payment = Payment.objects.create(**data)
    return payment


@pytest.fixture
def payment_pending_confirmation(db, supplier_01):
    """
    Creates a payment that is pending confirmation.
    It means there is an anticipation created/related
    and its status is 'PC'. Also, the original due_date
    must not have been reached.
    """
    due_date = date.today() + timedelta(days=10)
    new_due_date = date.today() + timedelta(days=5)
    data = {'supplier': supplier_01, 'due_date': due_date, 'value': 30}
    payment = Payment.objects.create(**data)

    new_value = calc_new_value(payment.pk, new_due_date.isoformat())
    antic_data = {'payment': payment, 'new_due_date': new_due_date, 'new_value': new_value}
    Anticipation.objects.create(**antic_data)
    return payment


@pytest.fixture
def payment_approved_anticipation(db, supplier_01):
    """
    Creates a payment for which an anticipation was approved.
    It means there is an anticipation created/related and its
    status is 'A'.
    """
    due_date = date.today() + timedelta(days=10)
    new_due_date = date.today() + timedelta(days=5)
    data = {'supplier': supplier_01, 'due_date': due_date, 'value': 40}
    payment = Payment.objects.create(**data)

    new_value = calc_new_value(payment.pk, new_due_date.isoformat())
    antic_data = {'payment': payment, 'new_due_date': new_due_date, 'new_value': new_value, 'status': 'A'}
    Anticipation.objects.create(**antic_data)
    return payment


@pytest.fixture
def payment_denied_anticipation(db, supplier_01):
    """
    Creates a payment for which an anticipation was denied.
    It means there is an anticipation created/related and its
    status is 'D'.
    """
    due_date = date.today() + timedelta(days=10)
    new_due_date = date.today() + timedelta(days=5)
    data = {'supplier': supplier_01, 'due_date': due_date, 'value': 50}
    payment = Payment.objects.create(**data)

    new_value = calc_new_value(payment.pk, new_due_date.isoformat())
    antic_data = {'payment': payment, 'new_due_date': new_due_date, 'new_value': new_value, 'status': 'D'}
    Anticipation.objects.create(**antic_data)
    return payment


@pytest.fixture
def payments_filter(payment_available_to_anticipate,
                    payment_unavailable_to_anticipate,
                    payment_pending_confirmation,
                    payment_approved_anticipation,
                    payment_denied_anticipation):
    payments = {'A': payment_available_to_anticipate,
                'U': payment_unavailable_to_anticipate,
                'PC': payment_pending_confirmation,
                'AN': payment_approved_anticipation,
                'D': payment_denied_anticipation}
    return payments


def test_filter_available_payments(auth_operator_01, payments_filter):
    """
    Certify the user can filter payments that
    are available to anticipate (status = 'A').
    """
    resp = auth_operator_01.get('/api/payments/', {'status': 'A'})
    assert PaymentSerializer(payments_filter['A']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['U']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['PC']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['AN']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['D']).data not in resp.data['results']


def test_filter_unavailable_payments(auth_operator_01, payments_filter):
    """
    Certify the user can filter payments that
    are unavailable to anticipate (status = 'U').
    """
    resp = auth_operator_01.get('/api/payments/', {'status': 'U'})
    assert PaymentSerializer(payments_filter['A']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['U']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['PC']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['AN']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['D']).data not in resp.data['results']


def test_filter_pending_conf_payments(auth_operator_01, payments_filter):
    """
    Certify the user can filter payments that
    has a pending confirmation anticipation (status = 'PC').
    """
    resp = auth_operator_01.get('/api/payments/', {'status': 'PC'})
    assert PaymentSerializer(payments_filter['A']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['U']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['PC']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['AN']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['D']).data not in resp.data['results']


def test_filter_anticipated_payments(auth_operator_01, payments_filter):
    """
    Certify the user can filter payments that
    has an approved anticipation (status = 'AN').
    """
    resp = auth_operator_01.get('/api/payments/', {'status': 'AN'})
    assert PaymentSerializer(payments_filter['A']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['U']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['PC']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['AN']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['D']).data not in resp.data['results']


def test_filter_denied_payments(auth_operator_01, payments_filter):
    """
    Certify the user can filter payments that
    has a denied anticipation (status = 'D').
    """
    resp = auth_operator_01.get('/api/payments/', {'status': 'D'})
    assert PaymentSerializer(payments_filter['A']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['U']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['PC']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['AN']).data not in resp.data['results']
    assert PaymentSerializer(payments_filter['D']).data in resp.data['results']


def test_no_filter_payments(auth_operator_01, payments_filter):
    """
    Certify that all payments are shown to an operator if no
    filters are applied.
    """
    resp = auth_operator_01.get('/api/payments/')
    assert PaymentSerializer(payments_filter['A']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['U']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['PC']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['AN']).data in resp.data['results']
    assert PaymentSerializer(payments_filter['D']).data in resp.data['results']
