from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def show_main_page(request):
    locations = Place.objects.all()
    places_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    for place in locations:
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
                    "detailsUrl": reverse('location', args=(place.slug,))
                }
            }
        )
    context = {'places_geojson': places_geojson}
    return render(request, template_name='index.html', context=context)


def get_location_details(request, slug):
    location = get_object_or_404(Place, slug=slug)
    print(location.latitude)
    location_details = {
        'title': location.title,
        'imgs': [image.image.url for image in location.image_set.all()],
        'description_short': location.description_short,
        'description_long': location.description_long,
        'coordinates': location.coordinates
    }
    return JsonResponse(location_details)
