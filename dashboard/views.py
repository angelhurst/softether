from rest_framework.views import APIView
from django.views import View
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
import subprocess
import json

def parsing(commad,):

    table = subprocess.check_output(commad, shell=True)
    table = table.decode('utf-8')

#     table="""IpTable command - Get the IP Address Table Database
# Item        |Value
# ------------+--------------------0
# ID          |3245080289
# Session Name|SID-SECURENAT-1
# IP Address  |192.168.30.1
# Created at  |2023-05-01 02:33:46
# Updated at  |2023-05-01 13:42:34
# Location    |On 'ip-172-26-10-68'
# ------------+--------------------0
# ID          |2294021727
# Session Name|SID-VPNUSER-[L2TP]-19
# IP Address  |192.168.30.10 (DHCP)
# Created at  |2023-05-01 13:30:46
# Updated at  |2023-05-01 13:42:34
# Location    |On 'ip-172-26-10-68'
# The command completed successfully."""

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

def parsing2(commad,):

    # table = subprocess.check_output(commad, shell=True)
    # table = table.decode('utf-8')

    table="""DhcpTable command - Get Virtual DHCP Server Function Lease Table of SecureNAT Function
Item            |Value
----------------+-------------------------
ID              |19
Leased at       |2023-05-01 (Mon) 14:10:47
Expires at      |2023-05-01 (Mon) 16:10:47
MAC Address     |CA-81-1B-57-E4-C2
Allocated IP    |192.168.30.10
Client Host Name|MacBook-Air-de-jose.local
The command completed successfully."""

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

    def get(self, request, format=None):

        table_ip = parsing('/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD iptable')
        table_dhcp = parsing('/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD dhcptable')

        device=[]
        for dhcp in table_dhcp:
            
            session = False

            for ip in table_ip:

                if dhcp['IP Address'] == ip['IP Address'].split(' ')[0]:
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
