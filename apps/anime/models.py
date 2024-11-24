from django.db import models
from django.core.validators import URLValidator

class Anime(models.Model):
    image = models.URLField(validators=[URLValidator])
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    episodes = models.PositiveIntegerField()
    members = models.PositiveIntegerField()
    rating = models.DecimalField(decimal_places=2)
    
    def __str__(self):
        return self.name
    