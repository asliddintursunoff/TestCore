from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from api.serializers.user_rating_serializer import LeaderboardUserSerializer,LeaderboardTeacherPanelSerializer
from api.models.userDB import User
from api.models.ClassicTestDB import ClassicTestDB
from api.models.ClasssicTestResultDB import ClassicTestSubmission,User
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=  ["Leader Board"])
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




        
class LeaderBoardForClassTestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaderboardTeacherPanelSerializer
    @extend_schema(tags=  ["Teacher Admin Panel"])
    def get(self, request, classic_test_id):
        classic_test = get_object_or_404(ClassicTestDB, id=classic_test_id, created_by=request.user)

        # Get all submissions for the test, ordered by score descending
        submissions = ClassicTestSubmission.objects.filter(test=classic_test).order_by('-total_score')

        # Serialize all submissions
        serializer = self.serializer_class(submissions, many=True)

        # Split into top 3 and others
        top_3 = serializer.data[:3]
        others = serializer.data[3:]

        return Response({
            "top_3": top_3,
            "others": others,
        }, status=status.HTTP_200_OK)
