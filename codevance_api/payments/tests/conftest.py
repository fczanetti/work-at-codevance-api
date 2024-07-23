import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from codevance_api.payments.models import Supplier


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
