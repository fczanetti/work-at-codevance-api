from decimal import Decimal


def calc_new_value(payment, new_date):
    """
    Calculates the new_value for a given payment.
    """
    diff_days = new_date - payment.due_date
    orig_value = Decimal(payment.value)
    interest_rate = Decimal('0.03')
    new_value = orig_value - (orig_value * (interest_rate / 30) * diff_days.days)
    return new_value
