from decimal import Decimal
from datetime import date

from codevance_api.payments.models import Payment, RequestLog
from codevance_api.payments.serializers import AnticipationSerializer, PaymentSerializer
from codevance_api.payments.tasks import send_email


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
        RequestLog.objects.create(anticipation=serializer.instance, user=request.user, action='R')

        send_email.delay_on_commit(sub='new_ant',
                                   recipient=[f'{serializer.instance.payment.supplier.user.email}'],
                                   ant_id=serializer.instance.id)

        return serializer.data


def create_payment(request):
    """
    Creates a payment and returns its data.

    """
    data = request.data.copy()

    # Get the correct supplier ID if it is a
    # supplier creating a new payment
    if not request.user.is_operator:
        data['supplier'] = request.user.supplier.pk

    serializer = PaymentSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data


def get_custom_queryset(user, status):
    """
    Returns the correct queryset to filter payments
    based on the URL parameter 'status'.
    - status = 'A': filter payments that are available to anticipate;
    - status = 'U': filter payments that are unavailable to anticipate;
    - status = 'PC': filter payments with pending confirmation anticipation;
    - status = 'AN': filter payments with anticipation approved (ANticipated);
    - status = 'D': filter payments with anticipation denied;
    - status = 'ALL': all payments are shown, filtered by supplier unless an
    operator is requesting. In this case, no filters are applied.
    """
    today = date.today()
    queryset = {
        'A': Payment.objects.select_related('supplier').filter(due_date__gt=today, anticipation=None),
        'U': Payment.objects.select_related('supplier')
        .filter(due_date__lte=today)
        .exclude(anticipation__status='A')
        .exclude(anticipation__status='D'),
        'PC': Payment.objects.select_related('supplier')
        .prefetch_related('anticipation')
        .filter(anticipation__status='PC')
        .filter(due_date__gt=today),
        'AN': Payment.objects.select_related('supplier')
        .prefetch_related('anticipation')
        .filter(anticipation__status='A'),
        'D': Payment.objects.select_related('supplier')
        .prefetch_related('anticipation')
        .filter(anticipation__status='D'),
        'ALL': Payment.objects.select_related('supplier')
    }
    if user.is_operator:
        return queryset[status].order_by('-creation_date')
    supplier = user.supplier
    return queryset[status].filter(supplier=supplier).order_by('-creation_date')
