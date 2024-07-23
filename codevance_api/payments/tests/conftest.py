from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from codevance_api.payments.models import Supplier, Payment


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
    supplier = Supplier.objects.create(user=user,
                                       corporate_name='Supplier 01',
                                       reg_number='111')
    return supplier


@pytest.fixture
def supplier_02(db):
    """
    Creates and returns a supplier.
    """
    User = get_user_model()
    user = User.objects.create(email='supplier_02@email.com')
    supplier = Supplier.objects.create(user=user,
                                       corporate_name='Supplier 02',
                                       reg_number='222')
    return supplier


@pytest.fixture
def auth_supplier_01(db, supplier_01):
    """
    Creates and returns an authenticated supplier.
    """
    client = APIClient()
    client.force_authenticate(user=supplier_01.user)
    return client


@pytest.fixture
def payment_supplier_01(supplier_01):
    """
    Creates and returns a payment that
    belongs to supplier 01.
    """
    due_date = date.today() + timedelta(days=10)
    payment = Payment.objects.create(supplier=supplier_01,
                                     due_date=due_date,
                                     value=1100)
    return payment


@pytest.fixture
def payment_supplier_02(supplier_02):
    """
    Creates and returns a payment that
    belongs to supplier 02.
    """
    due_date = date.today() + timedelta(days=10)
    payment = Payment.objects.create(supplier=supplier_02,
                                     due_date=due_date,
                                     value=1200)
    return payment
