from rest_framework import serializers
from api.models.userDB import User
from api.models.ClasssicTestResultDB import ClassicTestSubmission
class LeaderboardUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'XP_earned')

    def get_name(self, obj):
        return obj.telegram_name 
    


class LeaderboardTeacherPanelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = ClassicTestSubmission
        fields = ('user_id','name', 'total_score',"time_taken")

    def get_name(self, obj):
        return obj.user.telegram_name
    def get_user_id(self, obj):
        return obj.id 
    
