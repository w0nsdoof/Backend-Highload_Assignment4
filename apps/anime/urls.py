from django.urls import path
from .views import (
    upload_csv, upload_file_view, upload_status_view,
    AnimeListCreateView, AnimeRetrieveUpdateDestroyView,
)

from django.urls import path
from .views import upload_file_view, upload_status_view

urlpatterns = [
    path('upload/', upload_file_view, name='upload-file'),
    path('upload_status/<int:file_id>/', upload_status_view, name='upload-status'),
    
    path('anime/', AnimeListCreateView.as_view(), name='anime-list'),
    path('anime/<int:pk>/', AnimeRetrieveUpdateDestroyView.as_view(), name='anime-detail'),
]
