from django.urls import path
from payment.views import TestView
urlpatterns = [
    path('payme/endpoint/', TestView.as_view())
]