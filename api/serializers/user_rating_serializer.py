from rest_framework import serializers
from api.models.userDB import User

class LeaderboardUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'XP_earned')

    def get_name(self, obj):
        return obj.telegram_name 
