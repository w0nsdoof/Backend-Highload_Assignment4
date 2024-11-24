# forms.py
from django import forms
from .models import Anime, FileUpload

class AnimeForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Anime Name',
        widget=forms.TextInput(attrs={'placeholder': 'Search for an Anime'}))

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV files are allowed.")
        return uploaded_file
