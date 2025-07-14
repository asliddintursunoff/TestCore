from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.serializers.user_rating_serializer import LeaderboardUserSerializer
from api.models.userDB import User


class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.order_by('-XP_earned')
        serialized_users = LeaderboardUserSerializer(users, many=True).data

        # Top 3
        
        top_3 = [
            {"rank": j , **user}
            for j, user in enumerate(serialized_users[:3], start=1)
        ]
        # Others (ranked 4+)
        others = [
            {"rank": i , **user}
            for i, user in enumerate(serialized_users[3:], start=4)
        ]

        # Self info
        user_ids = [user["id"] for user in serialized_users]
        try:
            self_index = user_ids.index(request.user.id)
            self_info = {
                "rank": self_index + 1,
                "id":request.user.id,
                
                "name": request.user.telegram_name,
                "xp": request.user.XP_earned
            }
        except ValueError:
            self_info = None  # not in list? fallback if needed

        return Response({
            "top_3": top_3,
            "others": others,
            "self": self_info
        })
