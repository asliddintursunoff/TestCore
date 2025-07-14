from rest_framework import views,status,exceptions,permissions
from api.models.ClasssicTestResultDB import ClassicTestSubmission
from api.models.ClassicTestDB import ClassicTestDB
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from api.serializers.classic_test_result_serializer import TeacherPanelsTestDetailSerializer
from drf_spectacular.utils import extend_schema

class Classic_Test_Utils_Views(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeacherPanelsTestDetailSerializer
    @extend_schema(tags = ["Teacher Admin Panel"])
    def get(self,request,classic_test_id):
        user = request.user
        classic_test = get_object_or_404(ClassicTestDB,id = classic_test_id,created_by = user.id)
        classic_test_submitted = ClassicTestSubmission.objects.filter(test = classic_test)
        count_of_people_solved_test = classic_test_submitted.count()

        average_time = classic_test_submitted.aggregate(total_time=Sum('time_taken'))['total_time']//count_of_people_solved_test
        average_score = classic_test_submitted.aggregate(total_score_for_all=Sum('total_score'))['total_score_for_all']//count_of_people_solved_test
        data = {
            "student_number":count_of_people_solved_test,
            "average_score": average_score,
            "average_time": average_time
        }
        serializer = TeacherPanelsTestDetailSerializer(data)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        

