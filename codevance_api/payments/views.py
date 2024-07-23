from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from codevance_api.payments.models import Payment
from codevance_api.payments.serializers import PaymentSerializer


class PaymentListCreate(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_operator:
            return Payment.objects.filter(supplier__user=user).order_by('-creation_date')
        else:
            return Payment.objects.all().order_by('-creation_date')
