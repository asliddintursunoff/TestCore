from rest_framework import generics
from api.serializers.all_test_types import AllTestTypeSerializer
from api.models.test_typesDB import AllTestTypes
from drf_spectacular.utils import extend_schema,extend_schema_view

@extend_schema_view(
    get=extend_schema(tags=['Main page'],
                        summary="Getting all test types"))
class AllTestTypeListAPIView(generics.ListAPIView):
    serializer_class = AllTestTypeSerializer
    queryset = AllTestTypes.objects.all()