from django.urls import path

from codevance_api.payments.views import (PaymentListCreate, AnticipationCreate,
                                          AnticipationUpdate, PaymentRetrieve, RequestLogList)

urlpatterns = [
    path('payments/', PaymentListCreate.as_view()),
    path('payments/<int:pk>/', PaymentRetrieve.as_view()),
    path('anticipations/', AnticipationCreate.as_view()),
    path('anticipations/<int:pk>/', AnticipationUpdate.as_view()),
    path('logs/', RequestLogList.as_view()),

]
