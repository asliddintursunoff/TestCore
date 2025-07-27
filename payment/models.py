from django.db import models
from api.models import User,Tariff
# Create your models here.

class PaymentOrders(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
