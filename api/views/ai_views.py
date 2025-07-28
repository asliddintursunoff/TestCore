import requests
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.serializers.international_testSZ import QuestionDetailSerializer
from api.models.international_university_testDB import QuestionDB
from api.models.DTMtestDB import DTMQuestionDB
from rest_framework import status
from api.ai_logics.ai_connection_function import generate
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import serializers
import json
class AskResultResponseSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.CharField()
@extend_schema(
    tags=["AI Solve"],
    summary="Solve a question using AI",
    description="...",
    # parameters=[...],  # keep your existing parameters
    responses={
        200: AskResultResponseSerializer,
        404: OpenApiResponse(description="Question or test type not found"),
        500: OpenApiResponse(description="Internal error during AI generation"),
    }
)


class AskResultAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AskResultResponseSerializer

    def post(self, request, test_type_id, question_id):
        try:
            if test_type_id == 1:
                question_obj = QuestionDB.objects.get(id=question_id)
            elif test_type_id == 2:
                question_obj = DTMQuestionDB.objects.get(id=question_id)
            else:
                return Response({"error": "Test type id not found"}, status=status.HTTP_404_NOT_FOUND)
        except QuestionDB.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        prompt = f"""
        You are an expert math tutor. Solve the following question precisely.

        Question: {question_obj.question}

        Return the result ONLY as a JSON object with the following fields:
        - "answer": the correct final answer
        - "explanation": a clear step-by-step explanation

        Use this format:
        {{
          "answer": "...",
          "explanation": "..."
        }}

        Do not return anything else.
        """

        try:
            model_response = generate(prompt)  # Your Gemini model call
            parsed = json.loads(model_response.strip())

            return Response({
                "question": question_obj.question,
                "answer": parsed.get("answer"),
                "explanation": parsed.get("explanation")
            })

        except json.JSONDecodeError:
            return Response({"error": "Model did not return valid JSON", "raw": model_response}, status=500)
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

