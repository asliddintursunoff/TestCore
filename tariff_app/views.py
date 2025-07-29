from django.shortcuts import render
from api.models.tariffDB import Tariff
from rest_framework.generics import ListAPIView,RetrieveAPIView
from drf_spectacular.utils import extend_schema,extend_schema_view,OpenApiResponse
from .serializer import TariffSerializer,BuyingTariffSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated 

@extend_schema_view(
    get = extend_schema(tags=["Tariffs"],
                        responses= {200 : OpenApiResponse(TariffSerializer)})
)
class TarifListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TariffSerializer
    queryset = Tariff.objects.all()


@extend_schema_view(
    get = extend_schema(tags=["Tariffs"],
                        summary="Get a Payme link for Buying Tariff with its id",
                        responses= {200 : OpenApiResponse(BuyingTariffSerializer)})
)
class BuyingTariffRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyingTariffSerializer
    queryset = Tariff
    lookup_field = "id"

