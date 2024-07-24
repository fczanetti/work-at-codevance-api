from django.urls import path

from codevance_api.payments.views import PaymentListCreate, AnticipationCreate

urlpatterns = [
    path('payments/', PaymentListCreate.as_view()),
    path('anticipations/', AnticipationCreate.as_view())
]
