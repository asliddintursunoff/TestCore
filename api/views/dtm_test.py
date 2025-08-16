from rest_framework.views import APIView
from api.models.dtm_TEST import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import random
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse


class DTMTestFilterSerializer(serializers.Serializer):
    filter_type = serializers.CharField()
    language = serializers.CharField()
    first_subject = serializers.CharField()
    second_subject = serializers.CharField(required = False)


class GetDTMTestFilterPostRequest(APIView):
    permission_classes = [IsAuthenticated]
   
    @extend_schema(
        operation_id="get_dtm_test_filter",
        description="Return random tests based on filter_type.",
        request=DTMTestFilterSerializer,
        responses={
            # 200: OpenApiResponse(TestSetResponseSerializer),
            400: OpenApiResponse(description="Invalid data"),
            404: OpenApiResponse(description="Not found / wrong number"),
        },
        examples=[
            OpenApiExample(
                "Filter type 1 request",
                value={"filter_type": 1, "language": "uz", "first_subject": "Fizika", "second_subject": "Kimyo"},
                request_only=True,
            ),
            OpenApiExample(
                "Filter type 2 response",
                value={
                    "subject_1": {"id": 12, "subject_name": 3, "language": "uz"},
                    "subject_2": {"id": 34, "subject_name": 5, "language": "uz"},
                    "subject_3": {"id": 56, "subject_name": 7, "language": "uz"},
                    "subject_4": {"id": 78, "subject_name": 9, "language": "uz"},
                    "subject_5": {"id": 90, "subject_name": 11, "language": "uz"},
                },
                response_only=True,
            ),
        ],
    )
    def post(self,request):
        serializer = DTMTestFilterSerializer(data = request.data)    
        if serializer.is_valid():
            filter_type = serializer["filter_type"]
            language = serializer["language"]

            if filter_type == 1:
                
                first_subject = DTM_Subjects.objects.filter(subject_name = serializer["first_subject"],test_type = "main_subject").first()
                second_subject = DTM_Subjects.objects.filter(subject_name = serializer["second_subject"],test_type = "main_subject").first()
                test_1 = Test.objects.filter(subject_name = first_subject,language = language)
                random_idx = random.randint(0, test_1.objects.count() - 1)

                test_2 = Test.objects.filter(subject_name = second_subject,language = language)
                random_idy = random.randint(0, test_2.objects.count() - 1)
                test = {
                        "subject_1":test_1[random_idx],
                        "subject_2":test_2[random_idy]
                        }
                return Response(data=test,status=200)
            

            elif filter_type == 2:
                first_subject = DTM_Subjects.objects.filter(subject_name = serializer["first_subject"],test_type = "main_subject").first()
                second_subject = DTM_Subjects.objects.filter(subject_name = serializer["second_subject"],test_type = "main_subject").first()
                third_subject = DTM_Subjects.objects.filter(subject_name = "Matematika",test_type = "mandatory_subject").first()
                fourth_subject = DTM_Subjects.objects.filter(subject_name = "Ona tili",test_type = "mandatory_subject").first()
                fifth_subject = DTM_Subjects.objects.filter(subject_name = "Ingliz tili",test_type = "mandatory_subject").first()
                
                test_1 = Test.objects.filter(subject_name = first_subject,language = language)
                random_idx = random.randint(0, test_1.objects.count() - 1)

                test_2 = Test.objects.filter(subject_name = second_subject,language = language)
                random_idy = random.randint(0, test_2.objects.count() - 1)

                test_3 = Test.objects.filter(subject_name = third_subject,language = language)
                random_idz = random.randint(0, test_3.objects.count() - 1)

                test_4 = Test.objects.filter(subject_name = fourth_subject,language = language)
                random_ida = random.randint(0, test_4.objects.count() - 1)

                test_5 = Test.objects.filter(subject_name = fifth_subject,language = language)
                random_idb = random.randint(0, test_5.objects.count() - 1)

                test = {
                        "subject_1":test_1[random_idx],
                        "subject_2":test_2[random_idy],
                        "subject_3":test_3[random_idz],
                        "subject_4":test_4[random_ida],
                        "subject_5":test_5[random_idb],

                        }
                return Response(data=test,status=200)
            

            elif filter_type == 3:
                first_subject = DTM_Subjects.objects.filter(subject_name = serializer["first_subject"],test_type = "main_subject").first()
               
                test_1 = Test.objects.filter(subject_name = first_subject,language = language)
                random_idx = random.randint(0, test_1.objects.count() - 1)

                test = {
                        "subject_1":test_1[random_idx],
                        }
                return Response(data=test,status=200)
            
            else:
                Response(data= {"error":"You entered wrong number"},status=404)
        
        Response(data= {"error":"Invalid data"},status=404)
            