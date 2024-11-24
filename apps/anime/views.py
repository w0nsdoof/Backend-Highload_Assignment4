from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Anime
from .serializers import AnimeSerializer
from .utils import parse_csv

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100

class AnimeListCreateView(generics.ListCreateAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AnimeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [permissions.IsAuthenticated]

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'File is not in CSV format.'}, status=400)

        try:
            anime_objects = parse_csv(csv_file)

            Anime.objects.bulk_create(anime_objects)
            return JsonResponse({'success': f'{len(anime_objects)} records successfully uploaded.'}, status=201)
        
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'upload_csv.html')