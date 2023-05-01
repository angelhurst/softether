import subprocess
from os import system
import json


def parsing(commad):

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
# Session Name|SID-VPNUSER-[L2TP]-8
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

table_ip = parsing("/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD iptable")
table_dhcp = parsing("/usr/local/vpnserver/vpncmd /SERVER localhost:5555 /PASSWORD:holara2023 /HUB:myhub /CMD dhcptable")

print(json.dumps(table_ip, indent=4))
print(json.dumps(table_dhcp, indent=4))