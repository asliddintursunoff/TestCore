from rest_framework.views import APIView
from rest_framework import permissions
from api.models.ClasssicTestResultDB import ClassicTestSubmission
from api.serializers.international_test_resulltSZ import AnswerSubmission,TestSubmissionSerializer
from django.shortcuts import get_object_or_404
from api.models.ClassicTestDB import ClassicTestDB,ClassicQuestionDB,ClassicAnswerDB
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample,OpenApiParameter

@extend_schema(
    tags=["Classic Tests/Result"],
    summary="Submit answers for a test",
    description="Submit user's answers and time taken. .",
    request=TestSubmissionSerializer,
    responses={
        201: OpenApiResponse(
            description="Submission saved successfully",
            examples=[
                OpenApiExample(
                    name="classic Test Submission Success",
                    value={
                        "test_id": 5,
                        "success": True,
                        "submitted_test_id": 42
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Invalid data format")
    }
)
class ClassicTestSubmissionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestSubmissionSerializer
   
    def post(self,request):
        serializer = TestSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            test_id = serializer.validated_data["test_id"]
            time_taken = serializer.validated_data["time_taken"]
            answers = serializer.validated_data["answers"]
            test_instance = get_object_or_404(ClassicTestDB, id=test_id)
            submission = ClassicTestSubmission.objects.create(
                test = test_instance,user = user,time_taken = time_taken
            )
            
            total_correct = 0
          
            for answer in answers:
                is_correct_answer =False 
                question_id = answer["question_id"]
                answer_id = answer["chosen_answer_id"]
                try:
                    ClassicQuestionDB.objects.get(id = question_id)
                except ClassicQuestionDB.DoesNotExist:
                    raise NotFound(detail="Not found Question with this ID")
                
                if answer_id is None:
                    AnswerSubmission.objects.create(question_id = question_id,
                                                chosen_answer_id = None,
                                                submission = submission,
                                                is_correct_answer = False)
                try:
                    ClassicAnswerDB.objects.get(id = answer_id)
                except ClassicAnswerDB.DoesNotExist:
                    raise NotFound(detail="Not found Answer with this ID")

                try:
                    true_answer = ClassicAnswerDB.objects.filter(question_id = question_id,is_true = True).first()
                except ClassicAnswerDB.DoesNotExist:
                     raise NotFound(detail="There is no true answers for this question ID")
                
                if answer_id == true_answer.id:
                    total_correct+=1
                    is_correct_answer = True

                AnswerSubmission.objects.create(question_id = question_id,
                                                chosen_answer_id = answer_id,
                                                submission = submission,
                                                is_correct_answer = is_correct_answer)
                
            #Calculating XP based on correct answers
  
            submission.total_correct = total_correct
           
            submission.save()
            
            json_response = {
                "test_id":test_id,
                "success":True,
                "submitted_test_id":submission.id
            }
            return Response(json_response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

