from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from api.models.tariffDB import Tariff
class User(AbstractUser):
    active_tariff = models.ForeignKey(
        Tariff, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone_number = models.CharField(max_length=20,unique=True)
    telegram_id = models.CharField(max_length=50,unique=True,null=True,blank=True)
    tariff_expiry = models.DateTimeField(null=True, blank=True)
    def has_active_tariff(self):
        return self.active_tariff and self.tariff_expiry and timezone.now() < self.tariff_expiry



class OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        return (
            not self.used and 
            timezone.now() - self.created_at < timezone.timedelta(minutes=2)
        )
