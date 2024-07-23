from rest_framework import serializers

from codevance_api.payments.models import Payment, Supplier


class PaymentSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    class Meta:
        model = Payment
        fields = ['supplier', 'creation_date', 'due_date', 'value']
