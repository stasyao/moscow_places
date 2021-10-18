import os

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import URLValidator
import requests
from requests.exceptions import RequestException
from slugify import slugify

from .response_handler import decode_json_response
from .timer import timer
from places.models import Image, Place


@timer
def json_to_place(json_data):
    new_place_entry, created = Place.objects.get_or_create(
        **{'title': json_data['title'], 'slug': slugify(json_data['title']),
           'description_short': json_data['description_short'],
           'description_long': json_data['description_long'],
           'longitude': json_data['coordinates']['lng'],
           'latitude': json_data['coordinates']['lat']}
    )
    if not created:
        print(f'Локация {new_place_entry.title} уже есть в базе')
        return False
    for img_url in json_data['imgs']:
        img_name = os.path.basename(img_url)
        try:
            response = requests.get(img_url)
            response.raise_for_status()
            image_file = ContentFile(response.content)
            new_image_entry = Image(place=new_place_entry)
            img = new_image_entry.image
            img.save(img_name, image_file, save=False)
            new_image_entry.save()
        except RequestException as exc:
            print(f'Запрос к {img_url} не прошёл - {exc}')
    print(f'Создана запись о локации {new_place_entry.title}')
    return True


@timer
def json_url_to_place(url):
    validator = URLValidator()
    try:
        validator(url)
        try:
            json_to_place(decode_json_response(requests.get(url)))
            print('\nСоздана запись о локации')
        except RequestException as exc:
            print(f'Запрос к {url} не прошёл - {exc}')
    except ValidationError:
        print('Переданный путь не похож на URL')


@timer
def github_jsons_to_place(url):
    validator = URLValidator()
    try:
        validator(url)
        try:
            decoded_response = decode_json_response(requests.get(url))
            place_data_urls = [
                place_file['download_url'] for place_file in decoded_response
            ]
            place_data_json = []
            for url in place_data_urls:
                place_data_json.append(
                    decode_json_response(requests.get(url))
                )
            num_created = sum(
                json_to_place(json_data) for json_data in place_data_json
            )
            print(f'\nВсего записей о локациях создано: {num_created} ')
        except RequestException as exc:
            print(f'Запрос к {url} не прошёл - {exc}')
    except ValidationError:
        print('Переданный путь не похож на URL')
