from drf_spectacular.utils import extend_schema,extend_schema_view
from api.utils import calculating_earned_XP
from rest_framework import views
from api.models.test_result import TestDB,TestSubmission,AnswerDB,AnswerSubmission,QuestionDB
from rest_framework.response import Response
from rest_framework import status, permissions
from api.serializers.test_resultSZ import (
    TestSubmissionSerializer,SubmittedTestSerializer)
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound


class TestSubmissionAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestSubmissionSerializer
    @extend_schema(tags=["Test Result"])
    def post(self,request):
        serializer = TestSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            test_id = serializer.validated_data["test_id"]
            time_taken = serializer.validated_data["time_taken"]
            answers = serializer.validated_data["answers"]
            test_instance = get_object_or_404(TestDB, id=test_id)
            submission = TestSubmission.objects.create(
                test = test_instance,user = user,time_taken = time_taken
            )
            
            total_correct = 0
            total_questions = len(answers)
            for answer in answers:
                is_correct_answer =False 
                question_id = answer["question_id"]
                answer_id = answer["chosen_answer_id"]
                try:
                    QuestionDB.objects.get(id = question_id)
                except QuestionDB.DoesNotExist:
                    raise NotFound(detail="Not found Question with this ID")
                
                if answer_id is None:
                    AnswerSubmission.objects.create(question_id = question_id,
                                                chosen_answer_id = None,
                                                submission = submission,
                                                is_correct_answer = False)
                try:
                    AnswerDB.objects.get(id = answer_id)
                except AnswerDB.DoesNotExist:
                    raise NotFound(detail="Not found Answer with this ID")

                try:
                    true_answer = AnswerDB.objects.filter(question_id = question_id,is_true = True).first()
                except AnswerDB.DoesNotExist:
                     raise NotFound(detail="There is no true answers for this question ID")
                
                if answer_id == true_answer.id:
                    total_correct+=1
                    is_correct_answer = True

                AnswerSubmission.objects.create(question_id = question_id,
                                                chosen_answer_id = answer_id,
                                                submission = submission,
                                                is_correct_answer = is_correct_answer)
                
            #Calculating XP based on correct answers
            earned_XP = calculating_earned_XP(test_id,total_correct)
            
            submission.total_correct = total_correct
            submission.XP = earned_XP
            submission.save()
            4
            json_response = {
                "test_id":test_id,
                "success":True,
                "submitted_test_id":submission.id
            }
            return Response(json_response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


                

class TestSubmittedResultAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["Test Result"])
    def get(self,request,submitted_test_id):
        
        submitted_test = get_object_or_404(TestSubmission,test_id = submitted_test_id,user = request.user)
        test = submitted_test.test
        question_count = QuestionDB.objects.filter(
            subject__test=test
        ).count()
        data = {
            "id":test.id,
            "test_name":test.test_name,
            "time_for_test":test.time,
            "time_taken": submitted_test.time_taken,
            "total_correct_answer": submitted_test.total_correct,
            "total_questions":question_count,
            "XP_earned": submitted_test.XP,
            "subjects":[]
        }

        for subject in test.subjects.all():
            subject_data = {
                "subject_name": subject.subject_name,
                "questions": []
            }
            
            
                
            for question in subject.questions.all():
                answers_data = []
                chosen = AnswerSubmission.objects.filter(submission=submitted_test, question = question).first()
                is_correct_answered = False
                for answer in question.answers.all():
                    if chosen is not None and answer.id == chosen.chosen_answer :
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
                    #"get_answer_ai_link":"http://localhost:8000/api/users/5/",
                    "answers": answers_data
                })

            data["subjects"].append(subject_data)

        serializer = SubmittedTestSerializer(data, context={'request': request})
        return Response(serializer.data)



