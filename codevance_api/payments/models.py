from django.db import models
from django.contrib.auth import get_user_model

from codevance_api.payments.validators import date_not_before_today


class Supplier(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    corporate_name = models.CharField(max_length=128)
    reg_number = models.CharField(max_length=14, verbose_name='Company Registration Number',
                                  unique=True, help_text='Only numbers')


class Payment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(validators=[date_not_before_today])
    value = models.DecimalField(max_digits=11, decimal_places=2)


class Anticipation(models.Model):
    STATUS_CHOICES = {'A': 'Approved',
                      'PC': 'Pending confirmation',
                      'D': 'Denied'}
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    new_due_date = models.DateField(validators=[date_not_before_today])
    new_value = models.DecimalField(max_digits=11, decimal_places=2)
    update_date = models.DateField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='PC', max_length=25)


class RequestLog(models.Model):
    ACTION_CHOICES = {'A': 'Approval', 'D': 'Denial', 'R': 'Request'}
    anticipation = models.ForeignKey(Anticipation, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Registered in')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action = models.CharField(choices=ACTION_CHOICES, max_length=8)
