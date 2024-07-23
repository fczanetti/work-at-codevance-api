from django.urls import path

from codevance_api.payments.views import PaymentListCreate

urlpatterns = [
    path('payments/', PaymentListCreate.as_view())
]
