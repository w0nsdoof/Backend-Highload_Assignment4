from django.urls import path

from .views import (
    user_login, two_factor_verify, dashboard
)

app_name = 'authentication'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('2fa-verify/', two_factor_verify, name='2fa-verify'),
    path('dashboard/', dashboard, name='dashboard'),
]