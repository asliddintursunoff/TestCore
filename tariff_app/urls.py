from django.urls import path
from .views import TarifListAPIView,BuyingTariffRetrieveAPIView

urlpatterns = [
    path("all/",TarifListAPIView.as_view()),
    path("buy/<int:id>/",BuyingTariffRetrieveAPIView.as_view()),
]