from decimal import Decimal
from datetime import date

from codevance_api.payments.models import Payment
from codevance_api.payments.serializers import AnticipationSerializer
from rest_framework.serializers import ValidationError


def validate_date(dt):
    """
    Certifies the date (dt) informed:
    - is greater than or equal today;
    - has the expected ISO 8601 format.
    """
    if dt is None:
        raise ValidationError('You have to inform a date.')

    try:
        date.fromisoformat(dt)
    except ValueError:
        raise ValidationError('Make sure the date informed is in the correct format (YYYY-MM-DD).')

    if not date.fromisoformat(dt) >= date.today():
        raise ValidationError("Inform a date greater than or equal today.")


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
    payment_id = data.get('payment')

    new_due_date = data.get('new_due_date')
    validate_date(new_due_date)

    # Calculate new value
    new_value = calc_new_value(payment_id, new_due_date)
    data['new_value'] = new_value

    serializer = AnticipationSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data
