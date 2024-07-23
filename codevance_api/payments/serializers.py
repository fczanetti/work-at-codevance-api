from rest_framework import serializers

from codevance_api.payments.models import Payment, Supplier


class PaymentSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    class Meta:
        model = Payment
        fields = ['supplier', 'creation_date', 'due_date', 'value']

    def validate_value(self, value):
        """
        Certifies the value informed is greater than zero.
        """
        if not value > 0:
            raise serializers.ValidationError("Make sure the value is greater than zero.")
        return value
