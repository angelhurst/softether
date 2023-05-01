import subprocess
from os import system
import json

consulta  = "/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD iptable"
table_ip = subprocess.check_output(consulta, shell=True)
table_ip = table_ip.decode('utf-8')

# table_ip = """IpTable command - Get the IP Address Table Database
# Item        |Value
# ------------+--------------------
# ID          |3245080289
# Session Name|SID-SECURENAT-1
# IP Address  |192.168.30.1
# Created at  |2023-05-01 02:33:46
# Updated at  |2023-05-01 06:08:53
# Location    |On 'ip-172-26-10-68'
# ------------+--------------------
# ID          |28800360
# Session Name|SID-VPNUSER-[L2TP]-7
# IP Address  |192.168.30.10 (DHCP)
# Created at  |2023-05-01 05:40:23
# Updated at  |2023-05-01 06:08:55
# Location    |On 'ip-172-26-10-68'
# The command completed successfully."""

resultado = system(consulta)
item = table_ip.split('\n------------+--------------------\n')

data = []
for index_item in range(1,len(item)):
    session_keys = {}
    for index_key in item[index_item].split('\n'):

        if index_key.find('|') != -1:
            session_keys[index_key.split('|')[0].strip()]= index_key.split('|')[1].strip()
    
    data.append(session_keys)

print(json.dumps(data, indent=4))