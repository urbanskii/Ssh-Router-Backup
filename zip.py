import datetime
import os
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import shutil
from time import strftime
import time

@csrf_exempt
def newzip(request):
    date_time = strftime("%d%m%Y", time.localtime())

    city = request.POST.get('name')

    if city == 'lda' or 'aps':
        dir = '/home/data/Backup/BACKUP_'+ date_time
        path = os.path.exists(dir)
        if path == True:
            shutil.make_archive(dir, 'zip', dir)
            context = {
                'zipado': "Diretório: "+dir+" zipado!."
            }

            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))
        else:
            context = {
               'zipado': "Diretório: "+dir+" não existe!."
            }

            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))
    else:
            context = {
                'zipado': "Erro ao zipar!."
            }

            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))
