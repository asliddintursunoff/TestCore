# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.latex_generator import generate_pdf_response_from_json
from api.models.ClassicTestDB import ClassicTestDB
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.serializers.classic_testSZ import ClassicTestDBSerializer
from rest_framework import permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse



@extend_schema(
    tags=["Uploading Test PDF"],
    summary="Download a generated PDF for a test by its ID",
    description=(
        "This endpoint generates and returns a downloadable PDF file of a test, "
        "given the test's `classic_test_id`. The test data must already exist in the system."
    ),
    parameters=[
        OpenApiParameter(
            name="classic_test_id",
            description="ID of the ClassicTestDB object",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: OpenApiResponse(description="PDF file generated and returned as download"),
        404: OpenApiResponse(description="Test with provided ID not found"),
    }
)
class GetClassicTestPDFbyID(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, classic_test_id):
        test_instance = get_object_or_404(ClassicTestDB, id=classic_test_id)
        serializer = ClassicTestDBSerializer(test_instance)
        
        return generate_pdf_response_from_json(serializer.data)
