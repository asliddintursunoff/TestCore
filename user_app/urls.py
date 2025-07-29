from django.urls import path
from .views import HeaderDataAPIView
urlpatterns = [
    path("header/",HeaderDataAPIView.as_view())]