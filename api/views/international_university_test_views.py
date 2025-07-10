from drf_spectacular.utils import extend_schema,extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from api.serializers.international_testSZ import TestSerializer,TestDetailSerializer
from api.models.international_universityDB import FacultyDB
from api.models.international_university_testDB import TestDB
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        tags=['Internatinal University Tests'],
        summary="Get all tests belonging to a faculty",
        description="Provide a `faculty_id` to fetch all tests assigned to that faculty.",
        parameters=[
            OpenApiParameter(
                name="faculty_id",
                description="ID of the faculty",
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: OpenApiResponse(response=TestSerializer)
        }
    )
)
class TestsAPIView(APIView):
    permission_classes = [AllowAny]  
    def get(self,request,faculty_id):
        faculty = get_object_or_404(FacultyDB,id=faculty_id)
        serializer = TestSerializer(faculty)
        return Response(serializer.data)
    

#for get method
@extend_schema_view(
    get=extend_schema(
        tags=['Internatinal University Tests'],
        summary="Get a test by its ID",
        description="Provide a `test_id` to retrieve full details including subjects, questions, and answers.",
        parameters=[
            OpenApiParameter(
                name="id",
                description="ID of the test to retrieve",
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            )
        ],
        responses={200: TestDetailSerializer}
    )
)
class TestDetailAPIView(generics.RetrieveAPIView):
    queryset = TestDB.objects.all()
    serializer_class = TestDetailSerializer
    lookup_field = "id"


# for POST method
@extend_schema_view(
    post=extend_schema(
        tags=["Internatinal University Tests"],
        summary="Create a new test with full nested structure",
        description="Post a full JSON with subjects, questions, and answers to create a complete test.",
        request=TestDetailSerializer,
        responses={201: TestDetailSerializer}
    )
)
class FullTestCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = TestDB.objects.all()
    serializer_class = TestDetailSerializer

@extend_schema_view(
    put=extend_schema(
        tags=["Internatinal University Tests"],
        summary="Update a test entirely (PUT)"
    ),
    patch=extend_schema(
        tags=["Internatinal University Tests"],
        summary="Update part of a test (PATCH)"
    ),
)
class FullTestUpdateAPIView(generics.UpdateAPIView):
    queryset = TestDB.objects.all()
    serializer_class = TestDetailSerializer