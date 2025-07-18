from rest_framework import views,status,exceptions,permissions
from api.models.ClasssicTestResultDB import ClassicTestSubmission
from api.models.ClassicTestDB import ClassicTestDB
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from api.serializers.teacher_panel_serializer import ShareTestSerializer,TeacherPanelsTestDetailSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView

from rest_framework.exceptions import NotFound
from django.db.models import Sum
from rest_framework import views, status, permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema,extend_schema_view



class Classic_Test_Utils_Views(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeacherPanelsTestDetailSerializer

    @extend_schema(tags=["Teacher Admin Panel"])
    def get(self, request, classic_test_id):
        user = request.user

        # Fetch test or return 404
        classic_test = get_object_or_404(ClassicTestDB, id=classic_test_id, created_by=user.id)

        # Get submissions
        submissions = ClassicTestSubmission.objects.filter(test=classic_test)
        count = submissions.count()

        # Default values
        average_time = 0
        average_score = 0

        if count > 0:
            total_time = submissions.aggregate(total_time=Sum('time_taken'))['total_time'] or 0
            total_score = submissions.aggregate(total_score_for_all=Sum('total_score'))['total_score_for_all'] or 0

            # Avoid zero division
            average_time = total_time // count if total_time else 0
            average_score = total_score // count if total_score else 0

        data = {
            "students_number": count,
            "average_score": average_score,
            "average_time": average_time
        }

        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema_view(
    get = extend_schema(tags=["Teacher Admin Panel"])
)
class SHareTestRetrieveAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShareTestSerializer
    lookup_field = 'id' 
    def get_queryset(self):
        return ClassicTestDB.objects.filter(created_by = self.request.user)
   
