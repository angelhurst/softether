from rest_framework.views import APIView
from django.views import View
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.conf import settings
import subprocess
import json

def parsing(commad,):
    """recupera datos del vpn y los convierte a un dict

    Args:
        commad (string): comando que se ejecutara
    """

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

class ListDevice(APIView):
    """Api de Dispotivos conectados
    """

    def get(self, request, format=None):

        table_ip = parsing('/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:{} /HUB:{} /CMD iptable'.format(settings.VPN_PASS,settings.HUB))
        table_dhcp = parsing('/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:{} /HUB:{} /CMD dhcptable'.format(settings.VPN_PASS,settings.HUB))

        device=[]
        for dhcp in table_dhcp:
            
            session = False

            for ip in table_ip:

                if dhcp['Allocated IP'] == ip['IP Address'].split(' ')[0]:
                    device.append({
                        'status':'online',
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
                    'user':'',
                    'session_name':'',
                    'client_host': dhcp['Client Host Name'],
                    'ip_address': dhcp['Allocated IP'],
                    'mac_address':dhcp['MAC Address'],
                    'create_at':'',
                    'update_at':dhcp['Leased at'].split(' ')[0]+' '+ dhcp['Leased at'].split(' ')[2]

                })
        return Response(device)
    
class Home(View):
    initial = {"key": "value"}
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,self.initial)

