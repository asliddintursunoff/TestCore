from api.models.universityDB import UniversityDB,FacultyDB
from api.serializers.universitySZ import UniversitySerializer,FacultiesSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema_view,extend_schema



@extend_schema_view(
    get=extend_schema(tags=['University and Faculty'],
                        summary="Getting all university data as json"))
class UniversityListAPIView(generics.ListAPIView):
    queryset = UniversityDB.objects.all()
    serializer_class = UniversitySerializer

@extend_schema_view(
    get=extend_schema(tags=['University and Faculty'],
                        summary="Getting all FACULTIES belong to university id that is chosen"))
class FacultyListAPIView(generics.RetrieveAPIView):
    queryset = UniversityDB.objects.all()
    serializer_class = FacultiesSerializer
    lookup_field = 'id'

