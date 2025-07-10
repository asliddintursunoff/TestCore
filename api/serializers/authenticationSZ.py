from rest_framework import serializers
from api.models.userDB import User,OTP

class TelegramOTPStoreSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    phone_number = serializers.CharField()
    code = serializers.CharField()
    

class OTPVerifyCodeOnlySerializer(serializers.Serializer):
    code = serializers.CharField()