from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from api.models.userDB import User,Tariff
from .models import PaymentOrders
# from django 
class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        # user = User.objects.get(id = account["user_id"])
        # if not user:
        #     return self.ORDER_NOT_FOND
        
        order = PaymentOrders.objects.get(id = account["tariff_id"],is_paid = False)

        if not order.price:
            return self.ORDER_NOT_FOND
        if order.price*100 != amount:
            return self.INVALID_AMOUNT
        if not order:
            return self.ORDER_NOT_FOND
        
        return self.ORDER_FOUND
    
    def successfully_payment(self, account, transaction, *args, **kwargs):
        order = PaymentOrders.objects.filter(id = transaction.order_key).first()
        if not order:
            return self.ORDER_NOT_FOND
        order.is_finished = True
        order.save()
        

    def cancel_payment(self, account, transaction, *args, **kwargs):

        print(account)
      

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder

