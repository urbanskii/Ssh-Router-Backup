from django.http import HttpResponse
import assin
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import asyncio
import asyncssh


@csrf_exempt
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.POST.get('user')
        password = request.POST.get('password')

        try:
            loop = asyncio.new_event_loop()
            ss = loop.run_until_complete(assin.run_client(name, user, password))
            loop.close()

            print("retorno" + ss)
            if ss == "ok":
                context = {
                    'name': "Backup do equipamento: "+name+" Realizado com sucesso!."
                }
            else:
                context = {
                    'name': "erro" + ss
                }
            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))
        except (OSError, asyncssh.Error) as exc:

            context = {
                    'name': "erro:" + str(exc)
            }
            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())




