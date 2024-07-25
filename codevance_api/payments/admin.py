from django.contrib import admin

from codevance_api.payments.models import Supplier, Payment, Anticipation, RequestLog


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['user', 'corporate_name', 'reg_number']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'creation_date', 'due_date', 'value']


@admin.register(Anticipation)
class AnticipationAdmin(admin.ModelAdmin):
    list_display = ['payment', 'creation_date', 'new_due_date', 'new_value', 'update_date', 'status']


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['anticipation', 'created_at', 'user', 'action']
