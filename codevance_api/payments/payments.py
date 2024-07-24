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

    serializer = AnticipationSerializer(data=data, context={'request': request})
    if serializer.is_valid(raise_exception=True):

        payment_id = serializer.validated_data['payment'].pk
        new_due_date = serializer.validated_data['new_due_date']

        new_value = calc_new_value(payment_id, new_due_date.isoformat())

        serializer.save(new_value=new_value)
        return serializer.data
