from datetime import timedelta

from codevance_api.payments.payments import calc_new_value


def test_calc_new_value(payment_supplier_01):
    """
    Certifies that the new value is calculated correctly.
    """
    new_due_date = payment_supplier_01.due_date + timedelta(days=-15)
    new_value = calc_new_value(payment_supplier_01.pk, new_due_date.isoformat())
    assert new_value == 1083.5
