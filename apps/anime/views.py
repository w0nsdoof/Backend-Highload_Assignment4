from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

from .forms import AnimeForm
from .models import Anime

def create_anime_form(request):
    if request.method == 'POST':
        form = AnimeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            
            anime = Anime.objects.filter(name__icontains=name).first()
            if anime:
                ...
            else:
                ...
    else:
        form = AnimeForm()
        
    return render(request, 'anime_search.hmtl', {'form' : form})