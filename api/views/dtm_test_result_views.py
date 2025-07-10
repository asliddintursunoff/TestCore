from rest_framework import generics
from rest_framework import views
from api.models.dtm_test_result import *
from api.models.DTMtestDB import DTMSubject
from rest_framework.response import Response
from rest_framework import status,permissions
from api.serializers.dtm_test_resultSZ import DTMTestSubmissionSerializer,DTMSubmittedTestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema
from api.utils.calculating_XP import DTMcalculating_earned_XP
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample,OpenApiParameter


#for submitting dtm test answers
@extend_schema(
    tags=["DTM Test/Result"],
    summary="Submit answers for a DTM test",
    description=(
        "Submit a user's answers for a full DTM test. Each subject must include its answered questions. "
        "Calculates score, XP, and saves result."
    ),
    request=DTMTestSubmissionSerializer,
    responses={
        201: OpenApiResponse(
            description="Submission successful",
            examples=[
                {
                    "test_id": 3,
                    "success": True,
                    "submitted_test_id": 42
                }
            ]
        ),
        400: OpenApiResponse(description="Invalid input data"),
    }
)
class DTMTestSubmissionAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DTMTestSubmissionSerializer

    def post(self,request):
        serializer = DTMTestSubmissionSerializer(data = request.data)
        if serializer.is_valid():
            user = request.user
            test_id = serializer.validated_data["test_id"]
            time_taken = serializer.validated_data["time_taken"]
            subjects = serializer.validated_data["subjects"]

            test_instance = get_object_or_404(DTMTestDB,id = test_id)
            submission = DTMTestSubmission.objects.create(user = user,
                                                          test = test_instance,
                                                          time_taken = time_taken)
            total_score = 0
            total_correct_answer = 0
            for subject in subjects:
                
                total_correct = 0
                subject_id = subject["dtm_subject_id"]
                subject_instance = get_object_or_404(DTMSubject,id = subject_id)
                answers = subject["answers"]
                submitted_subject = DTMSubjectsSubmissionDB.objects.create(total_correct_answered = 0,
                                                                           score = 0,
                                                                           submission = submission,
                                                                           dtm_subject_id = subject_instance.id)


                for answer  in answers:
                    is_correct_answer = False
                    question_id = answer["question_id"]
                    chosen_answer_id = answer["chosen_answer_id"]
                    
                    question_instance = get_object_or_404(DTMQuestionDB,id = question_id)
                    chosen_answer_instance = get_object_or_404(DTMAnswerDB,id = chosen_answer_id)

                    try:
                        true_answer = DTMAnswerDB.objects.filter(question_id = question_id,is_true = True).first()
                    except DTMAnswerDB.DoesNotExist:
                        raise NotFound(detail="There is no true answers for this question ID")
                    
                    if chosen_answer_id == true_answer.id:
                        total_correct +=1
                        is_correct_answer = True

                    DTMAnswerSubmission.objects.create(question_id = question_id,
                                                       chosen_answer_id = chosen_answer_id,
                                                       submission_subject = submitted_subject,
                                                       is_correct_answer = is_correct_answer)
                
                earned_score_for_this_subject = total_correct*subject_instance.subject_score
                
                
                submitted_subject.total_correct_answered = total_correct
                submitted_subject.score = earned_score_for_this_subject
                submitted_subject.save()
                total_score+=earned_score_for_this_subject
                total_correct_answer+=total_correct


            earned_XP = DTMcalculating_earned_XP(test_id,total_correct_answer)
            submission.XP = earned_XP
            submission.total_score = total_score
            submission.save()
            json_response = {
                "test_id":test_id,
                "success":True,
                "submitted_test_id":submission.id
            }
            return Response(json_response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


                    
#for getting submitted test answers   
@extend_schema(
    tags=["DTM Test/Result"],
    summary="Get result of submitted DTM test",
    description="Returns detailed result for a previously submitted test including score, XP, and per-question answers.",
    parameters=[
        OpenApiParameter(
            name="submitted_dtm_test_id",
            description="The ID of the submitted DTM test result",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: DTMSubmittedTestSerializer,
        404: OpenApiResponse(description="Submitted test not found"),
    }
)
class DTMTestSubmittedResultAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self,request,submitted_dtm_test_id):
        submitted_test = get_object_or_404(DTMTestSubmission,id = submitted_dtm_test_id)
        test = submitted_test.test
       
        question_count = DTMQuestionDB.objects.filter(subject__dtm_test = test).count()
        data = {
            "dtm_test_id":test.id,
            "test_name":test.dtm_test_name,
            "time_for_test":test.time,
            "time_taken": submitted_test.time_taken,
            "total_score": submitted_test.total_score,
            "total_questions":question_count,
            "XP_earned": submitted_test.XP,
            "subjects":[]
        }

        for subject in test.DTMsubjects.all():
            sub = DTMSubjectsSubmissionDB.objects.filter(dtm_subject_id = subject.id,submission = submitted_test).first()
            subject_data = {
                "subject_name":subject.subject_name,
                "subject_score_for_each_question":subject.subject_score,
                "total_earned_score":sub.score,
                "number_total_correct":sub.total_correct_answered,

                "questions":[]
            }
            
            for question in subject.DTMquestions.all():
                answers_data = []
                chosen = DTMAnswerSubmission.objects.filter(submission_subject = sub,question = question).first()
                is_correct_answered = False
                for answer in question.DTManswers.all():
                    if chosen is not None and answer.id == chosen.chosen_answer:
                        is_correct_answered = True

                    
                    answers_data.append({
                            "id": answer.id,
                            "answer": answer.answer,
                            "answer_picture": answer.answer_picture,
                            "is_true_answer": answer.is_true,      
                        })

                subject_data["questions"].append({
                        "id": question.id,
                        "question": question.question,
                        "question_img": question.question_img,
                        "chosen_answer_id": chosen.chosen_answer_id if chosen else None,
                        "answered_correctly" : is_correct_answered,
                        
                        "answers": answers_data
                    })  
            data["subjects"].append(subject_data)
        serializer = DTMSubmittedTestSerializer(data, context={'request': request})
        return Response(serializer.data)


