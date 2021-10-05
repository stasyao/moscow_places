from django.http.response import HttpResponse
from django.template import loader


def show_start_page(request):
   template = loader.get_template('index.html')
   return HttpResponse(
      template.render(None)
   )
