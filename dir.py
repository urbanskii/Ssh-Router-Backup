import datetime
import os
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from time import strftime
import time

@csrf_exempt
def newdir(request):
    date_time = strftime("%d%m%Y", time.localtime())

    city = str(request.POST.get('name'))

    dirMAINcheck= '/home/data/Backup/BACKUP_'+date_time

    path1 = os.path.exists(dirMAINcheck)

    if path1 == True:

        if (city == 'ttt' or city == 'ttt'):

            dir = '/home/data/Backup/BACKUP_'+date_time+'/'+city+'DTC_'+ date_time
          
            path = os.path.exists(dir)

            if path == False:
                os.mkdir(dir)
                context = {
                    'diretorio': "Diretório: "+dir+" criado!."
                }

                template = loader.get_template('home.html')
                return HttpResponse(template.render(context, request))
            else:
                context = {
                    'diretorio': "Diretório: "+dir+" já está Criado!."
                }

                template = loader.get_template('home.html')
                return HttpResponse(template.render(context, request))
        elif city == "ttt" or "ttt" or "ttt":
            dir1 = '/home/data/Backup/BACKUP_' + date_time + '/' + city + 'OLT_' + date_time

            path = os.path.exists(dir1)

            if path == False:
                os.mkdir(dir1)
                context = {
                    'diretorio': "Diretório: " + dir1 + " criado!."
                }

                template = loader.get_template('home.html')
                return HttpResponse(template.render(context, request))
            else:
                context = {
                    'diretorio': "Diretório: " + dir1 + " já está Criado!."
                }

                template = loader.get_template('home.html')
                return HttpResponse(template.render(context, request))

        else:
            context = {
                'diretorio': "Erro ao criar diretório"+dir+"!."
            }

            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))

    else:
        context = {
            'diretorio': "Diretório principal do dia não está criado!."
        }

        template = loader.get_template('home.html')
        return HttpResponse(template.render(context, request))

@csrf_exempt
def dirMain(request):
    date_time = strftime("%d%m%Y", time.localtime())
    folder = str(request.POST.get('name'))


    if folder == "BACKUP":
        dir = '/home/data/Backup/BACKUP_'+date_time
        path = os.path.exists(dir)

        if path == False:
            os.mkdir(dir)
            context = {
                'diretorioMain': "Diretório: " + dir + " criado!."
            }

            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))
        else:
            context = {
                'diretorioMain': "Diretório: " + dir + " já está Criado!."
            }

            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))
    else:
        context = {
            'diretorioMain': "Erro ao criar diretório!."
        }

        template = loader.get_template('home.html')
        return HttpResponse(template.render(context, request))
