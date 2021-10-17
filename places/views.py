from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def show_main_page(request):
    places = Place.objects.all()
    places_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    for place in places:
        places_geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.longitude, place.latitude]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.pk,
                    "detailsUrl": reverse('place', args=(place.slug,))
                }
            }
        )
    context = {'places_geojson': places_geojson}
    return render(request, template_name='index.html', context=context)


def get_place_details(request, slug):
    place = get_object_or_404(Place, slug=slug)
    place_details = {
        'title': place.title,
        'imgs': [image.image.url for image in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {'lng': place.longitude, 'lat': place.latitude}
    }
    return JsonResponse(
        place_details, json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )
