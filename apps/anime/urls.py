from django.urls import path
from .views import (
    upload_csv,
    AnimeListCreateView, AnimeRetrieveUpdateDestroyView
)

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('anime/', AnimeListCreateView.as_view(), name='anime-list'),
    path('anime/<int:pk>/', AnimeRetrieveUpdateDestroyView.as_view(), name='anime-detail'),
]
