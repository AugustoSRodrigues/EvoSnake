import requests
import time
import sys
import json

baseurl = 'http://127.0.0.1:8181/onos/v1/'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

def create_fwdrule(deviceid, src_prt, dst_prt):
    flow_data = {
            "priority": 40001,
            "timeout": 0,
            "isPermanent": True,
            "deviceId": deviceid,
            "treatment": {"instructions": [{"type": "OUTPUT", "port": dst_prt}]},
            "selector": {"criteria": [{"type": "IN_PORT", "port": src_prt}]}
        }
    r = requests.post(baseurl + 'flows/{0}'.format(deviceid), data=json.dumps(flow_data), auth=('karaf', 'karaf'), headers=headers)
    print(r.status_code)
    if r.status_code == 201:
        print( "Sucesso criando regra no switch \"{0}\": porta {1} -> porta {2}".format(deviceid, src_prt, dst_prt) )
    else:
        print( "Falha ao adicionar regra para switch \"{0}\": porta {1} -> porta {2}".format(deviceid, src_prt, dst_prt) )
    

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print('''\
numero errado de parametros!
uso:
    python3 api-controller.py <host1> <host2>''')
        exit()

    host1 = sys.argv[1]
    host2 = sys.argv[2]

    ### vamos logo encontrar um caminho e criar regras para ele ###

    #primeiro precisamos saber os switches aos quais os hosts estao conectados e em quais portas
    r = requests.get(baseurl + 'hosts/{0}'.format(host1), auth=('karaf', 'karaf'))
    s1 = r.json()['locations'][0]['elementId']
    s1h1_port = r.json()['locations'][0]['port']

    r = requests.get(baseurl + 'hosts/{0}'.format(host2), auth=('karaf', 'karaf'))
    print(r.content)
    s2 = r.json()['locations'][0]['elementId']
    s2h2_port = r.json()['locations'][0]['port']

    #vamos conectar e ficar monitorando se hosts permanecem conectados
    connected = False
    connlinks = []

    while True:
        #primeiro conectam
        if not connected:
            #vamos encontrar o melhor caminho entre esses switches
            print("Encontrando melhor caminho")
            r = requests.get(baseurl + 'paths/{0}/{1}'.format(s1, s2), auth=('karaf', 'karaf'))
            print(baseurl + 'paths/{0}/{1}'.format(s1, s2))
            connlinks = r.json()['paths'][0]['links']

            src_port = s1h1_port
            for link in connlinks:
                switchid = link['src']['device']
                dst_port = link['src']['port']

                #IDA
                create_fwdrule(switchid, src_port, dst_port)        

                #VOLTA
                create_fwdrule(switchid, dst_port, src_port)

                switchid = link['dst']['device']
                src_port = link['dst']['port']

            create_fwdrule(switchid, src_port, s2h2_port)
            create_fwdrule(switchid, s2h2_port, src_port)
            connected = True

        #fica monitorando os links
        #r = requests.get(baseurl + 'links', auth=('karaf', 'karaf'))
        #availlinks = r.json()['links']
        #for link in connlinks:
        #    if link in availlinks:
        #        continue
        #    print("Algum link entre os hosts foi perdido, recalculando conexao...")
        #    connected = False
        #time.sleep(5)
        








        