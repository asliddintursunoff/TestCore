import requests
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from api.serializers.international_testSZ import QuestionDetailSerializer
from api.models.international_university_testDB import QuestionDB
from api.models.DTMtestDB import DTMQuestionDB
from rest_framework import status
from api.ai_logics.ai_connection_function import generate
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

@extend_schema(
    tags=["AI Solve"],
    summary="Solve a question using AI",
    description=(
        "Provide a `test_type_id` and `question_id` to get an AI-generated explanation and result.\n\n"
        "`test_type_id=1` = International university test question, `test_type_id=2` = DTM question.\n"
        "Returns the original question and a detailed answer."
    ),
    parameters=[
        OpenApiParameter(
            name="test_type_id",
            description="1 for International university test, 2 for DTM test",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
        OpenApiParameter(
            name="question_id",
            description="ID of the question to solve",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={
        200: OpenApiResponse(
            description="Question and AI-generated answer",
            examples=[
                {
                    "question": "What is 2 + 2?",
                    "answer": "The answer is 4. Because 2 added to 2 equals 4."
                }
            ]
        ),
        404: OpenApiResponse(description="Question or test type not found"),
        500: OpenApiResponse(description="Internal error during AI generation"),
    }
)
class AskResultAPIView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request,test_type_id, question_id):
        try:
            if test_type_id == 1:
                question_obj = QuestionDB.objects.get(id=question_id)

            elif test_type_id==2:
                question_obj = DTMQuestionDB.objects.get(id = question_id)
            else:
                return Response({"error":"Test type id not found"},status=status.HTTP_404_NOT_FOUND)
            
        except QuestionDB.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        prompt = f"solve this question and give exact result with clear instructions {question_obj.question}"
       
        try:
            answer = generate(prompt)
            return Response({
                "question": question_obj.question,
                "answer": answer
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)










# class AskResultAPIView(APIView):
#     permission_classes = [AllowAny] 
#     def post(self, request,test_type_id, question_id):
#         try:
#             if test_type_id == 1:
#                 question_obj = QuestionDB.objects.get(id=question_id)

#             elif test_type_id==2:
#                 question_obj = DTMQuestionDB.objects.get(id = question_id)
#             else:
#                 return Response({"error":"Test type id not found"},status=status.HTTP_404_NOT_FOUND)
            
#         except QuestionDB.DoesNotExist:
#             return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

#         prompt = f"solve this question and give exact explanation and  true answer do not include other extra wordss {question_obj.question}"

#         payload = {
#             "model": OLLAMA_MODEL,
#             "prompt": prompt,
#             "stream": False
#         }

#         try:
#             res = requests.post(OLLAMA_URL, json=payload)
#             res.raise_for_status()
#             answer = res.json().get("response", "").strip()
#             return Response({
#                 "question": prompt,
#                 "answer": answer
#             })
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

