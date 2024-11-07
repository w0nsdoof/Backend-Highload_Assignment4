from django.urls import path
from .views import send_email_view

urlpatterns = [
    path('email/', send_email_view),
]