from api.models.international_universityDB import UniversityDB,FacultyDB

from api.serializers.international_universitySZ import UniversitySerializer,FacultiesSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema_view,extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema




@extend_schema_view(
    get=extend_schema(
        tags=["International University and Faculty"],
        summary="Get all international universities",
        description="Returns a list of all international universities, including name, short name, and image.",
        responses={
            200: OpenApiResponse(response=UniversitySerializer, description="List of universities")
        }
    )
)
class UniversityListAPIView(generics.ListAPIView):
    queryset = UniversityDB.objects.all()
    serializer_class = UniversitySerializer

@extend_schema_view(
    get=extend_schema(
        tags=["International University and Faculty"],
        summary="Get all faculties by university ID",
        description="Returns all faculties that belong to the university identified by the provided ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                description="ID of the university",
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: OpenApiResponse(response=FacultiesSerializer, description="Faculties for the selected university"),
            404: OpenApiResponse(description="University not found"),
        }
    )
)
class FacultyListAPIView(generics.RetrieveAPIView):
    queryset = UniversityDB.objects.all()
    serializer_class = FacultiesSerializer
    lookup_field = 'id'

