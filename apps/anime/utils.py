import csv
from .models import Anime

def parse_csv(file):
    """
    Parse the uploaded CSV file, validate the headers, and return Anime objects.
    """
    try:
        data_set = file.read().decode('UTF-8')
        csv_reader = csv.reader(data_set.splitlines(), delimiter=',')

        headers = next(csv_reader, None)
        if not headers:
            raise ValueError('CSV file is empty or missing headers.')

        header_map = {header.strip(): index for index, header in enumerate(headers)}

        required_headers = {'name', 'genre', 'type', 'episodes', 'rating', 'members'}
        if not required_headers.issubset(header_map.keys()):
            missing_headers = required_headers - header_map.keys()
            raise ValueError(f'Missing required headers: {missing_headers}')

        anime_objects = []
        for row in csv_reader:
            try:
                anime = Anime(
                    name=row[header_map['name']],
                    genre=row[header_map['genre']],
                    type=row[header_map['type']],
                    episodes=int(row[header_map['episodes']]),
                    rating=float(row[header_map['rating']]),
                    members=int(row[header_map['members']])
                )
                anime_objects.append(anime)
            except (ValueError, IndexError) as e:
                raise ValueError(f"Error processing row {row}: {str(e)}")

        return anime_objects

    except Exception as e:
        raise ValueError(f"Error reading CSV file: {str(e)}")
