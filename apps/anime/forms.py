# forms.py
from django import forms
from .models import Anime

class AnimeForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Anime Name',
        widget=forms.TextInput(attrs={'placeholder': 'Search for an Anime'}))
