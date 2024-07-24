from decimal import Decimal
from datetime import date

from codevance_api.payments.models import Payment
from codevance_api.payments.serializers import AnticipationSerializer


def calc_new_value(payment_id, new_date):
    """
    Calculates the new_value for a given payment.
    """
    payment = Payment.objects.get(id=payment_id)
    diff_days = payment.due_date - date.fromisoformat(new_date)
    orig_value = Decimal(payment.value)
    interest_rate = Decimal('0.03')
    new_value = orig_value - (orig_value * (interest_rate / 30) * diff_days.days)
    return round(new_value, 2)


def create_anticipation(request):
    """
    Creates an anticipation and returns its data.
    """
    data = request.data.copy()
    payment_id = data['payment']
    new_due_date = data['new_due_date']

    # Calculate new value
    new_value = calc_new_value(payment_id, new_due_date)
    data['new_value'] = new_value

    serializer = AnticipationSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data
