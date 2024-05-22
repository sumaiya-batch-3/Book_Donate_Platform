from django.db import models
from author.models import UserAccount
from .constants import TRANSACTION_TYPE
from django.contrib.auth.models import User
# Create your models here.


class Transaction(models.Model):
    account=models.ForeignKey(UserAccount,related_name='transactions',on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction=models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type=models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp'] 