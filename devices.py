def device(request):

	if request == 'yourhost':
		ip = '192.168.0.x'
	return ip


def comandos(request):

	if request == 'yourhost':
		command=['show version',]
	return comandos

