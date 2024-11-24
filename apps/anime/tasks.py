import csv
from celery import shared_task
from .models import FileUpload, Anime

@shared_task
def process_csv_file(file_upload_id):
    file_upload = FileUpload.objects.get(id=file_upload_id)
    try:
        file_upload.status = 'processing'
        file_upload.save()

        with open(file_upload.file.path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            headers = next(csv_reader)  
            if not headers:
                raise ValueError('CSV file is empty or missing headers.')

            # Map headers to their respective index positions
            header_map = {header.strip().lower(): index for index, header in enumerate(headers)}

            required_headers = {'name', 'genre', 'type', 'episodes', 'rating', 'members'}
            if not required_headers.issubset(header_map.keys()):
                missing_headers = required_headers - header_map.keys()
                raise ValueError(f'Missing required headers: {missing_headers}')

            processed = 0
            total_rows = sum(1 for row in csv_reader)  
            f.seek(0)  
            next(csv_reader)  

            for row in csv_reader:
                try:
                    Anime.objects.create(
                        name=row[header_map['name']],
                        genre=row[header_map['genre']],
                        type=row[header_map['type']],
                        episodes=int(row[header_map['episodes']]),
                        rating=float(row[header_map['rating']]),
                        members=int(row[header_map['members']])
                    )
                    processed += 1

                    # Update progress percentage
                    file_upload.progress = int((processed / total_rows) * 100)
                    file_upload.save()

                except (ValueError, IndexError) as e:
                    raise ValueError(f"Error processing row {row}: {str(e)}")

        file_upload.status = 'completed'
        file_upload.save()

    except Exception as e:
        file_upload.status = 'failed'
        file_upload.error_message = str(e)
        file_upload.save()
