from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def show_main_page(request):
   locations = Place.objects.all()
   features = []
   for loc in locations:
      features.extend(
         [
            {
               "type": "Feature",
               "geometry": {
                  "type": "Point",
                  "coordinates": [float(v) for v in loc.coordinates.values()]
               },
               "properties": {
                  "title": loc.title,
                  "placeId": loc.id,
                  "detailsUrl": reverse('location', args=(loc.pk,))
               }
            }
         ]
      )
   places_geojson = {
      "type": "FeatureCollection",
      "features": features
   }
   context = { 'places_geojson': places_geojson }
   return render(request, template_name='index.html', context=context)


def get_location_details(request, place_id):
   location = get_object_or_404(Place, pk=place_id)
   location_details = {
         'title': location.title,
         'imgs': [image.image.url for image in location.image_set.all()],'description_short': location.description_short,
         'description_long': location.description_long,
         'coordinates': location.coordinates
      }
   return JsonResponse(location_details)
