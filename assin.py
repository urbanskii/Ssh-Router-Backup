import asyncssh
import time
import devices
import os
from time import strftime
import asyncio
import paramiko


@asyncio.coroutine
async def save_output(process, request, cmd):
    date_time = strftime("%d%m%Y", time.localtime())

    if (request[0:3] == 'LDA' or request[0:3] == 'APS'):
        dir = '/home/data/Backup/BACKUP_'+date_time+'/'+request[0:6]+'_'+ date_time+'/'
        path = os.path.exists(dir)
    elif request[0:3] == 'APU' or request[0:3] == 'CAB' or request[0:3] == 'RLA':
        dir = '/home/data/Backup/BACKUP_'+date_time+'/'+request[0:3]+'OLT_'+ date_time+'/'
        path = os.path.exists(dir)
    path = str(dir)
    output = ''
    get=''
    try:
        if request[0:3] == 'CAB' or request[0:3] == 'APU' or request[0:3] == 'RLA':
            if cmd == 'display ipv6 neighbors' or cmd == 'display current-configuration':
                while True:
                    get = await process.stdout.readline()
                    if get[32:38] == 'Static':
                        break
                    if get[:6] == 'return':
                        break
                    output = output + get
            else:
                output = await process.stdout.readuntil("#")
        else:

            if request[6:11] == 'RTD03' or request[6:11] == 'RTD04' or request[6:11] == 'CMT04':
                if cmd == 'display ipv6 neighbors' or cmd == 'display current-configuration' or cmd == 'show running-config verbose full' \
                        or cmd == 'display ipv6 routing-table protocol direct' or  cmd == 'display ipv6 routing-table protocol static':
                    while True:
                        get = await process.stdout.readline()
                        if get[32:38] == 'Static':
                            break
                        if get[:6] == 'return':
                            break
                        if get[:29] == 'configure slot 13 no shutdown':
                            break
                        if get[62:65] == ' R ':
                            break
                        output = output + get
                else:
                    if request[6:11] == 'RTD03' or request[6:11] == 'RTD04':
                        output = await process.stdout.readuntil(">")
                    else:
                        output = await process.stdout.readuntil(request + "#")
            else:
                    output = await process.stdout.readuntil(request + "#")

        with open(path + request + '_' + date_time + '.txt', 'a+') as f:
            f.write(output[:])
            output= ''
            print(output[:])
            return "ok"
    except (OSError, ) as exc:
        return str(exc)

async def run_client(request, user, password):
    date_time = strftime("%d%m%Y", time.localtime())
    if (request[0:3] == 'LDA' or request[0:3] == 'APS'):
        dir = '/home/data/Backup/BACKUP_'+date_time+'/'+request[0:6]+'_'+ date_time+'/'
        path = os.path.exists(dir)
    if request[0:3] == 'APU' or request[0:3] == 'CAB' or request[0:3] == 'RLA':
        dir = '/home/data/Backup/BACKUP_'+date_time+'/'+request[0:3]+'OLT_'+ date_time+'/'
        path = os.path.exists(dir)

    if path == True:

        if request[:11] == 'APSDTCRTD01'or request[:11] == 'LDADTCCMT06':
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(devices.device(request), port=22, username=user, password=password, look_for_keys='', timeout=200 * 60)
            connection = ssh.invoke_shell()
            output=''
            stdout= connection.recv(64).decode(encoding='utf-8')
            outFile = open(dir + request + '_' + date_time+'.txt', "w")
            outFile.write(stdout[:])

            comandos = devices.comandos(request)
            for p in comandos:
                connection.send(p + '\n')
                time.sleep(2)
                if p == 'Show running-config':
                    time.sleep(10)
                stdout= connection.recv(2500000).decode(encoding='utf-8')
                output = output + stdout
                print (output[:])
            outFile = open(dir + request + '_' + date_time+'.txt', "a+")
            outFile.write(output[:]+ '\n')
            return 'ok'
        else:

            async with asyncssh.connect(devices.device(request), port=22, username=user, password=password, known_hosts=None, client_keys=None) as conn:
                process = await conn.create_process()
                print ("passei")
                if request[0:3] == 'APU' or request[0:3] == 'CAB' or request[0:3] == 'RLA':
                    output = ''
                    output = await  process.stdout.readuntil(">")
                    outFile = open(dir + request + '_' + date_time+'.txt', "w")
                    comandos = devices.comandos(request)
                    outFile.write(output+ '\n')

                    for cmd in comandos:
                        process.stdin.write(cmd + '\n')
                        await save_output(process, request, cmd)
                    return "ok"
                else:
                    if request[6:11] == 'RTD03' or request[6:11] == 'RTD04':
                        output = await  process.stdout.readuntil(">")
                        outFile = open(dir + request + '_' + date_time + '.txt', "w")
                    elif request[6:11] == 'CMT06':

                        output = await  process.stdout.readuntil(request)
                        outFile = open(dir + request + '_' + date_time + '.txt', "w")
                    else:

                        output = await  process.stdout.readuntil("*")
                        outFile = open(dir + request + '_' + date_time + '.txt', "w")


                    comandos = devices.comandos(request)
                    outFile.write(output + '\n')

                    for cmd in comandos:
                        print (cmd)
                        if cmd == 'show running-config verbose full':
                            process.stdin.write(cmd + '\n')

                            await save_output(process, request, cmd)
                        else:
                            process.stdin.write(cmd + '\n')
                            await save_output(process, request, cmd)
                    return "ok"
    else:
        return "Pasta não está criada!."












