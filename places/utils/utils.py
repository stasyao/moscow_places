from datetime import timedelta
import os
import time

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import URLValidator
import requests

from places.models import Image, Place


def timer(func):
    def quantify(*args, **kwargs):
        start_time = time.monotonic()
        func(*args, **kwargs)
        end_time = time.monotonic()
        duration = timedelta(seconds=end_time - start_time)
        print(f'Время выполнения - {duration}')
    return quantify


def json_to_place(json_data):
    data_for_place_model = {
        key: value for key, value in json_data.items() if key != 'imgs'
    }
    new_place_entry, created = Place.objects.get_or_create(
        **data_for_place_model
    )
    if created:
        print(f'Создана запись о локации {new_place_entry.title}')
        for img_url in json_data['imgs']:
            img_name = os.path.basename(img_url)
            res = requests.get(img_url)
            image_file = ContentFile(res.content)
            new_image_entry = Image(location=new_place_entry)
            img = new_image_entry.image
            img.save(img_name, image_file, save=False)
            new_image_entry.save()
        return True
    print(f'Локация {new_place_entry.title} уже есть в базе')
    return False


@timer
def json_url_to_place(url):
    validator = URLValidator()
    try:
        validator(url)
        try:
            res = requests.get(url)
            res.raise_for_status()
            json_to_place(res.json())
            print('\nСоздана запись о локации')
        except Exception as exc:
            print(f'Запрос к {url} не прошёл - {exc}')
    except ValidationError:
        print('Переданный путь не похож на URL')


@timer
def github_jsons_to_place(url):
    validator = URLValidator()
    try:
        validator(url)
        try:
            res = requests.get(url)
            res.raise_for_status()
            place_data_urls = [
                place_file['download_url'] for place_file in res.json()
            ]
            place_data_json = [
                requests.get(url).json() for url in place_data_urls
            ]
            num_created = 0
            for json_data in place_data_json:
                if json_to_place(json_data):
                    num_created += 1
            print(f'\nВсего записей о локациях создано: {num_created} ')
        except Exception as exc:
            print(f'Запрос к {url} не прошёл - {exc}')
    except ValidationError:
        print('Переданный путь не похож на URL')
