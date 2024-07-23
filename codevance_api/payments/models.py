from django.db import models
from django.contrib.auth import get_user_model


class Supplier(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    corporate_name = models.CharField(max_length=128)
    reg_number = models.CharField(max_length=14, verbose_name='Company Registration Number',
                                  unique=True, help_text='Only numbers')


class Payment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    value = models.DecimalField(max_digits=11, decimal_places=2)


class Anticipation(models.Model):
    STATUS_CHOICES = {'A': 'Approved',
                      'PC': 'Pending confirmation',
                      'D': 'Denied'}
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    creation_date = models.DateField()
    new_due_date = models.DateField()
    new_value = models.DecimalField(max_digits=11, decimal_places=2)
    update_date = models.DateField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='PC', editable=False, max_length=25)
