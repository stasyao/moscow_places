from django.http.response import HttpResponse
from django.template import loader

from django.logger import logger

def show_start_page(request):
   logger.info('SHOW_START')
   template = loader.get_template('index.html')
   return HttpResponse(
      template.render(None)
   )
