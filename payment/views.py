from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from api.models.userDB import User,Tariff
from .models import PaymentOrders
# from django 
class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        try:
            order = PaymentOrders.objects.get(id=account["order_id"], is_paid=False)
        except (PaymentOrders.DoesNotExist, KeyError, TypeError):
            return self.ORDER_NOT_FOND  # Proper Paycom error: -31050

        if int(order.price * 100) != int(amount):
            return self.INVALID_AMOUNT  # Proper Paycom error: -31001

        return self.ORDER_FOUND  # Paycom expects {"allow": True}

    def successfully_payment(self, account, transaction, *args, **kwargs):
        try:
            order = PaymentOrders.objects.get(id=transaction.order_key)
        except PaymentOrders.DoesNotExist:
            return self.ORDER_NOT_FOND

        order.is_paid = True
        order.save()

    def cancel_payment(self, account, transaction, *args, **kwargs):

        print(account)
      

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder

