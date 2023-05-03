import subprocess
from os import system
import json

def parsing(commad,):

    table = subprocess.check_output(commad, shell=True)
    table = table.decode('utf-8')

    separtor = ""
    for row in table.split('\n'):
        if row.find('-+-') != -1:
            separtor = row


    item = table.split(separtor)

    data = []
    for index_item in range(1,len(item)):
        session_keys = {}
        for index_key in item[index_item].split('\n'):

            if index_key.find('|') != -1:
                session_keys[index_key.split('|')[0].strip()]= index_key.split('|')[1].strip()
        
        data.append(session_keys)
    return(data)


table_ip = parsing('/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD iptable')
table_dhcp = parsing('/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD dhcptable')

device=[]
for dhcp in table_dhcp:
    
    session = False

    for ip in table_ip:

        id_ip= ip['Session Name'].split('-')[len(ip['Session Name'].split('-'))-1]

        if dhcp['ID'] == id_ip:
            device.append({
                'status':'online',
                'id':dhcp['ID'],
                'user':ip['Session Name'].split('-')[1],
                'session_name': ip['Session Name'],
                'client_host': dhcp['Client Host Name'],
                'ip_address': dhcp['Allocated IP'],
                'mac_address':dhcp['MAC Address'],
                'create_at':ip['Created at'],
                'update_at':ip['Updated at']

            })
            session =True
    
    if session is not True:
        device.append({
            'status':'offline',
            'id':dhcp['ID'],
            'user':'',
            'session_name':'',
            'client_host': dhcp['Client Host Name'],
            'ip_address': dhcp['Allocated IP'],
            'mac_address':dhcp['MAC Address'],
            'create_at':'',
            'update_at':dhcp['Leased at'].split(' ')[0]+' '+ dhcp['Leased at'].split(' ')[2]

        })

print(device)

#  sudo `which python` manage.py runserver 172.26.10.68:8000