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
def create_place_record(payload: dict):
    new_place_entry, created = Place.objects.get_or_create(
        **{'title': payload['title'], 'slug': slugify(payload['title']),
           'description_short': payload['description_short'],
           'description_long': payload['description_long'],
           'longitude': payload['coordinates']['lng'],
           'latitude': payload['coordinates']['lat']}
    )
    if not created:
        print(f'Локация {new_place_entry.title} уже есть в базе')
        return False
    for img_url in payload['imgs']:
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
def create_place_record_from_json(url):
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        print('Переданный путь не похож на URL')
    try:
        create_place_record(decode_json_response(requests.get(url)))
        print('\nСоздана запись о локации')
    except RequestException as exc:
        print(f'Запрос к {url} не прошёл - {exc}')


@timer
def create_place_record_from_github_jsons(url):
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        print('Переданный путь не похож на URL')
    try:
        decoded_response = decode_json_response(requests.get(url))
        place_json_urls = [
            place['download_url'] for place in decoded_response
        ]
        place_decoded: list[dict] = [
            decode_json_response(requests.get(url)) for url in
            place_json_urls
        ]
        num_created = sum(
            create_place_record(json_data) for json_data in place_decoded
        )
        print(f'\nВсего записей о локациях создано: {num_created} ')
    except RequestException as exc:
        print(f'Запрос к {url} не прошёл - {exc}')
