from rest_framework import serializers
from api.models.tariffDB import Tariff
from payment.models import PaymentOrders
from paycomuz import Paycom
paycom = Paycom()




class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['tariff_name','tariff_price','duration_days','description']
        
        

class BuyingTariffSerializer(serializers.ModelSerializer):
    payme_link = serializers.SerializerMethodField()
    class Meta:
        model = Tariff
        fields = ['payme_link']

    def get_payme_link(self,obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        try:
            user = request.user
            order = PaymentOrders.objects.create(user=user, tariff=obj)
            amount = obj.tariff_price
            url = paycom.create_initialization(
                amount=amount,
                order_id=str(order.id),
                return_url='https://testcore.uz/'
            )
            return url
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})