from drf_spectacular.utils import extend_schema,extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from api.serializers.international_testSZ import TestSerializer,TestDetailSerializer,TestBaseSerializer
from api.models.international_universityDB import FacultyDB
from api.models.international_university_testDB import TestDB
from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from rest_framework import status
from api.models.international_university_test_result import TestSubmission
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
    permission_classes = [IsAuthenticated]  
    def get(self,request,faculty_id):
        faculty = get_object_or_404(FacultyDB,id=faculty_id)
        serializer = TestSerializer(faculty)
        return Response(serializer.data)
    

    
@extend_schema_view(
    get=extend_schema(
        tags=['Internatinal University Tests'],
       
        parameters=[
            OpenApiParameter(
                name="id",
                description="ID of the test",
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
class TestDetailRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TestBaseSerializer
    queryset = TestDB.objects.all()
    lookup_field = 'id'



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


@extend_schema_view(
    get = extend_schema(
        tags=['International University Tests'],
        summary="Get a test ID by faculty ID",
        description="Provide a `faculty_id` to retrieve a random test ID that the user has not submitted yet.",
        parameters=[
            OpenApiParameter(
                name="faculty_id",
                description="ID of the faculty to retrieve the test from",
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: OpenApiResponse(
                response=None,
                description="Returns the test ID if found, along with success status."
            ),
            204: OpenApiResponse(
                response=None,
                description="No available tests found for the user."
            ),
            404: OpenApiResponse(
                response=None,
                description="Faculty not found."
            ),
            500: OpenApiResponse(
                response=None,
                description="Unexpected server error."
            ),
        }
    )
)
class TestChooseAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self, request, faculty_id):
        try:
            user = request.user

            try:
                faculty = FacultyDB.objects.get(id=faculty_id)
            except FacultyDB.DoesNotExist:
                return Response({"success": False, "error": "Faculty not found."}, status=status.HTTP_404_NOT_FOUND)

            submitted_tests = TestSubmission.objects.filter(user=user).values_list('test_id', flat=True)

            if faculty.university.is_faculty_based:
                base_tests = TestDB.objects.filter(faculty=faculty)
            else:
                base_tests = TestDB.objects.filter(university_root=faculty.university)

            tests = base_tests.exclude(id__in=submitted_tests) if submitted_tests.exists() else base_tests

            test = tests.first()
            if not test:
                return Response({"success": False, "message": "No available tests found."}, status=status.HTTP_204_NO_CONTENT)
      
            

            serialized_test = TestBaseSerializer(test).data

            return Response(serialized_test, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"success": False, "error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










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