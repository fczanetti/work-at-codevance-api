from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from codevance_api.payments.models import Payment
from codevance_api.payments.serializers import PaymentSerializer


class PaymentListCreate(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
