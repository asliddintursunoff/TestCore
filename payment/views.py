from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from api.models.userDB import User,Tariff
from .models import PaymentOrders
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# from django 
class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        try:
            order = PaymentOrders.objects.get(id=account["order_id"], is_paid=False)
        except (PaymentOrders.DoesNotExist, KeyError, TypeError):
            return self.ORDER_NOT_FOND  # Proper Paycom error: -31050

        if int(order.tariff.tariff_price * 100) != int(amount):
            return self.INVALID_AMOUNT  # Proper Paycom error: -31001

        return self.ORDER_FOUND  # Paycom expects {"allow": True}

    def successfully_payment(self, account, transaction, *args, **kwargs):
        try:
            order = PaymentOrders.objects.get(id=transaction.order_key)
        except PaymentOrders.DoesNotExist:
            return self.ORDER_NOT_FOND
        try:
            order.is_paid = True
            user = order.user
            tariff = order.tariff
            user.active_tariff = tariff
            now = timezone.now()
            user.tariff_expiry = now + timedelta(days=tariff.duration_days)
            
            user.save()
            order.save()
        except Exception as e:
            logger.error(f"ERROR in payment confirm: {str(e)}",exc_info=True)
            return self.ORDER_NOT_FOND

    def cancel_payment(self, account, transaction, *args, **kwargs):

        print(account)
      

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder

