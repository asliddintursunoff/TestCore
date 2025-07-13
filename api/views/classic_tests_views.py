
from api.models.ClassicTestDB import ClassicTestDB
from rest_framework import generics
from rest_framework import permissions
from api.serializers.classic_testSZ import ClassicBaseTestSerializer


class ClassicTestListAPIView(generics.ListAPIView):
    serializer_class = ClassicBaseTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ClassicTestDB.objects.filter(created_by=self.request.user)

    

