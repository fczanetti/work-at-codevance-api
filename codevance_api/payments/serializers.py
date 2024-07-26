from rest_framework import serializers

from codevance_api.payments.models import Payment, Supplier, Anticipation, RequestLog


class PaymentSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'supplier', 'creation_date', 'due_date', 'value']

    def validate_value(self, value):
        """
        Certifies the value informed is greater than zero.
        """
        if not value > 0:
            raise serializers.ValidationError("Make sure the value is greater than zero.")
        return value


class AnticipationSerializer(serializers.ModelSerializer):
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all())

    class Meta:
        model = Anticipation
        fields = ['id', 'payment', 'creation_date', 'new_due_date', 'new_value', 'update_date', 'status']
        read_only_fields = ['new_value']

    def validate_payment(self, value):
        """
        Certifies that the payment_id informed
        belongs to the supplier creating the
        anticipation.
        """
        user = self.context['request'].user
        if user.is_operator:
            return value
        if not Payment.objects.filter(id=value.pk).filter(supplier__user=user).exists():
            raise serializers.ValidationError("Make sure you informed a valid payment ID.")
        return value


class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = ['id', 'anticipation', 'created_at', 'user', 'action']
