from django.db import models
from django.core.validators import URLValidator

png = "https://sun9-45.userapi.com/impg/WzIHXgWw1mCv9FlhBYT3SwuRiX87nQ16yGQ5SA/6wF4X83rUss.jpg?size=384x384&quality=96&sign=4755dd761ff818b1eff4e3e476679a6e&type=album"

class Anime(models.Model):
    image = models.URLField(validators=[URLValidator], default=png)
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    episodes = models.PositiveIntegerField()
    members = models.PositiveIntegerField()
    rating = models.DecimalField(decimal_places=2,max_digits=10)
    
    def __str__(self):
        return self.name

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, completed, failed
    progress = models.PositiveIntegerField(default=0)  # Percentage
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.file.name} ({self.status})"
    
    