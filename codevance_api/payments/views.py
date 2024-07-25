from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from codevance_api.payments.models import Anticipation
from codevance_api.payments.payments import create_anticipation, create_payment, get_custom_queryset
from codevance_api.payments.permissions import RequestPermission
from codevance_api.payments.serializers import PaymentSerializer, AnticipationSerializer


class PaymentListCreate(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, RequestPermission]

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', 'ALL')
        queryset = get_custom_queryset(user, status)
        return queryset

    def post(self, request, *args, **kwargs):
        new_payment_data = create_payment(self.request)
        return Response(new_payment_data, status=HTTP_201_CREATED)


class AnticipationCreate(generics.CreateAPIView):
    serializer_class = AnticipationSerializer
    permission_classes = [IsAuthenticated, RequestPermission]

    def post(self, request, *args, **kwargs):
        new_anticipation_data = create_anticipation(self.request)
        return Response(new_anticipation_data, status=HTTP_201_CREATED)


class AnticipationUpdate(generics.UpdateAPIView):
    serializer_class = AnticipationSerializer
    permission_classes = [IsAuthenticated, RequestPermission]

    def get_queryset(self):
        id = self.kwargs['pk']
        user = self.request.user
        if user.is_operator:
            return Anticipation.objects.filter(id=id)
        return Anticipation.objects.filter(payment__supplier__user=user).filter(id=id)
