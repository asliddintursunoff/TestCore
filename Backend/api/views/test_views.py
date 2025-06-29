from drf_spectacular.utils import extend_schema,extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from api.serializers.testSZ import TestSerializer,TestDetailSerializer
from api.models.universityDB import FacultyDB
from api.models.testDB import TestDB
from rest_framework.permissions import AllowAny


@extend_schema_view(
    get=extend_schema(tags=['Test'],
                        summary="Get multiple tests belong to faculty with faculty_id ",
                        description="By entering faculty id you can take all tests belong to that FACULTY"))
class TestsAPIView(APIView):
    permission_classes = [AllowAny]  
    def get(self,request,faculty_id):
        faculty = get_object_or_404(FacultyDB,id=faculty_id)
        serializer = TestSerializer(faculty)
        return Response(serializer.data)
    

#for get method
@extend_schema_view(
    get=extend_schema(tags=['Test'],
                        summary="Get a test based on its id",
                        description="By entering test id you can take test belong to that id")  )
class TestDetailAPIView(generics.RetrieveAPIView):
    queryset = TestDB.objects.all()
    serializer_class = TestDetailSerializer
    lookup_field = "id"


# for POST method
@extend_schema_view(
    post=extend_schema(tags=['CRUD TESTS'],
                       summary="For creating TEST"),
)
class FullTestCreateAPIView(generics.CreateAPIView):
    queryset = TestDB.objects.all()
    serializer_class = TestDetailSerializer

@extend_schema_view(
    put=extend_schema(tags=['CRUD TESTS'],
                       summary="For updating TEST"),
    patch=extend_schema(tags=['CRUD TESTS'],
                       summary="For updating TEST"),
)
class FullTestUpdateAPIView(generics.UpdateAPIView):
    queryset = TestDB.objects.all()
    serializer_class = TestDetailSerializer