from celery import shared_task
from .models import FileUpload, Anime
from .utils import parse_csv
import time


@shared_task
def process_csv_file(file_upload_id):
    file_upload = FileUpload.objects.get(id=file_upload_id)
    try:
        file_upload.status = 'processing'
        file_upload.save()

        anime_objects = parse_csv(file_upload.file.path)
        total = len(anime_objects)

        for index, anime in enumerate(anime_objects):
            anime.save()
            file_upload.progress = int(((index + 1) / total) * 100)
            file_upload.save()
            
            time.sleep(0.003)

        file_upload.status = 'completed'
        file_upload.save()

    except Exception as e:
        file_upload.status = 'failed'
        file_upload.error_message = str(e)
        file_upload.save()
