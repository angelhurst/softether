import subprocess
from os import system
import json


def parsing(commad):

    table = subprocess.check_output(commad, shell=True)
    table = table.decode('utf-8')

    item = table.split('\n------------+--------------------\n')

    data = []
    for index_item in range(1,len(item)):
        session_keys = {}
        for index_key in item[index_item].split('\n'):

            if index_key.find('|') != -1:
                session_keys[index_key.split('|')[0].strip()]= index_key.split('|')[1].strip()
        
        data.append(session_keys)
    return(data)

table_ip = parsing("/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD iptable")
table_dhcp = parsing("/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD dhcptable")

print(json.dumps(table_ip, indent=4))
print(json.dumps(table_dhcp, indent=4))