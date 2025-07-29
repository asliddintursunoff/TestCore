from django.shortcuts import render

from api.models.userDB import User
from rest_framework.views import APIView
from .serializer import HeaderDataSerialzier
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema,extend_schema_view


@extend_schema_view(
    get = extend_schema(tags=["Header"],
                        )
)
class HeaderDataAPIView(APIView):
    serializer_class = HeaderDataSerialzier
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        serializer = HeaderDataSerialzier(
            {"user_tariff":user.active_tariff.tariff_name,
             "user_tariff_free": user.active_tariff.is_free,
             "user_xp":user.XP_earned}
        )

        return Response(serializer.data,status=200)



