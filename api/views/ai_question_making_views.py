from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializers.PDF_serializer import PDFuploadSerializer
from api.utils.extracting_text_from_pdf import extract_individual_questions,all_question_joined_from_file,grouping_questions
from api.ai_logics.ai_connection_function import generate,generate_async,number_of_all_api_tokens
from rest_framework import permissions

import asyncio
from api.ai_logics.ai_requests_text import asking_seperating_questions_from_AI,ask_ai_to_generate_new_questions
from api.utils.calculating_XP import merge_questions
# from drf_spectacular.utils import extend_schema,extend_schema_view
from api.serializers.classic_testSZ import ClassicTestDBSerializer
from datetime import datetime
from drf_spectacular.utils import extend_schema,extend_schema_view
from drf_spectacular.utils import OpenApiExample, OpenApiResponse


today = datetime.now().date()




async def test_take_calling_async(lst, size):
    tasks = [
        generate_async(asking_seperating_questions_from_AI(lst[i:i + size]))
        for i in range(0, len(lst), size)
    ]
    results = await asyncio.gather(*tasks)
    # Filter out None (failed generations)
    return [r for r in results if r is not None]

async def test_create_calling_async(lst, size):
    tasks = [
        generate_async(ask_ai_to_generate_new_questions(lst[i:i + size]))
        for i in range(0, len(lst), size)
    ]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]


@extend_schema_view(
    post=extend_schema(
        request=PDFuploadSerializer,
        tags=['AI Tests from Entering File'],
        summary="Upload a PDF to auto-generate a test",
        description="This endpoint accepts a PDF file containing exam questions, extracts them using AI, and saves them as a structured test under the current user.",
       
        responses={
            201: OpenApiResponse(response=ClassicTestDBSerializer, description="Test successfully created from file"),
            400: OpenApiResponse(description="Bad request (e.g. invalid file or data format)"),
        }
    )
)

class TakingQuestionFromFileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request, *args, **kwargs):
        serializer = PDFuploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file_upload']

            temp_path = f"temp_{file.name}"
            with open(temp_path, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            extracted_questions_from_file = all_question_joined_from_file(temp_path)
            taking_seperate_questions_as_list = extract_individual_questions(extracted_questions_from_file)
            token_number = number_of_all_api_tokens()
            chunk_size = max(1, len(taking_seperate_questions_as_list) // token_number)

            questions_lst = asyncio.run(test_take_calling_async(taking_seperate_questions_as_list,chunk_size))
            final_json  =merge_questions(questions_lst)
            final_json["test_name"] = f"{today}-{file.name}"
            user = request.user
            final_json["created_by"] = user.id
           
 
            
            serializer = ClassicTestDBSerializer(data=final_json)

            if serializer.is_valid():
                test_obj = serializer.save()
                return Response({"id": test_obj.id,"test":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        request=PDFuploadSerializer,
        tags=['AI Tests from Entering File'],
        summary="Upload a PDF to auto-generate a test",
        description="This endpoint accepts a PDF file containing exam questions, extracts them using AI, and saves them as a structured test under the current user.",
        responses={
            201: OpenApiResponse(response=ClassicTestDBSerializer, description="Test successfully created from file"),
            400: OpenApiResponse(description="Bad request (e.g. invalid file or data format)"),
        }
    )
)

class CreatingNewQuestionFromFileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
 
    def post(self, request, *args, **kwargs):
        serializer = PDFuploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file_upload']

            temp_path = f"temp_{file.name}"
            with open(temp_path, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            extracted_questions_from_file = all_question_joined_from_file(temp_path)
            taking_seperate_questions_as_list = extract_individual_questions(extracted_questions_from_file)
            token_number = number_of_all_api_tokens()
            chunk_size = max(1, len(taking_seperate_questions_as_list) // token_number)

            questions_lst = asyncio.run(test_create_calling_async(taking_seperate_questions_as_list,chunk_size))
            final_json  =merge_questions(questions_lst)

            final_json  = merge_questions(questions_lst)
            final_json["test_name"] = f"{today}-{file.name}"
            user = request.user
            final_json["created_by"] = user.id
            serializer = ClassicTestDBSerializer(data=final_json)

            if serializer.is_valid():
                serializer.save()  

                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    
    