import json
import yaml
import requests
import http.client

config = open("setup_config.yaml", "r")
configInput = yaml.load(config,  Loader=yaml.FullLoader)
f5saasUsername = configInput['f5cs_username']
f5saasPassword = configInput['f5cs_password']
my_service_instance_name = configInput['service_instance_name']
my_lbr_name = configInput['lbr_name']
my_lbr_aliases = configInput['lbr_aliases']
my_virtual_servers = configInput['virtual_servers']
my_pools = configInput['pools']
my_monitors = configInput['monitors']
checkInterval = configInput['checkInterval']
enternal_ip_query_servers = configInput['ip_query']

def login():
    global token
    url = "https://api.cloudservices.f5.com/v1/svc-auth/login"
    headers = {'Content-Type': 'application/json'}
    payload = {'username': f5saasUsername, 'password': f5saasPassword}
    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    ##print(response)
    token = response.json()['access_token']
    if response.status_code != 200:
        print ("Login Failed")
        logging.warning('Login Failed')
    ##print(response.json()['access_token'])
    return response.json()['access_token']

d = {
"service_instance_name": my_service_instance_name,
"deleted": False,
"service_type": "gslb",
"configuration": {
"gslb_service": {
"load_balanced_records": {
my_lbr_name: {
"aliases": [
my_lbr_aliases
],
"display_name": my_lbr_name,
"enable": True,
"persist_cidr_ipv4": 24,
"persist_cidr_ipv6": 56,
"persistence": True,
"persistence_ttl": "3600",
"proximity_rules": [
{
"pool": my_pools,
"region": "global",
"score": 1
}
],
"rr_type": "A"
}
},
"monitors": {
my_monitors: {
"display_name": my_pools,
"monitor_type": "icmp_standard",
"remark": "Ping Check"
}
},
"pools": {
my_pools: {
"display_name": my_pools,
"enable": True,
"load_balancing_mode": "static-persist",
"max_answers": 1,
"members": [
{
"virtual_server": my_virtual_servers,
"monitor": "basic"
}
],
"remark": "",
"rr_type": "A",
"ttl": 30,
}
},
"virtual_servers": {
my_virtual_servers: {
"address": "1.1.1.1",
"display_name": my_virtual_servers,
"monitor": my_monitors,
"port": "80",
"virtual_server_type": "cloud"
}
}, "zone": my_service_instance_name
}
}
}
def dnslb_push():
    payload = json.dumps(d, indent=4)
    conn = http.client.HTTPSConnection("api.cloudservices.f5.com")
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + token + ''}
    conn.request("PUT", "/v1/svc-subscription/subscriptions/s-aaBcUfzic6", payload, headers)
    response = conn.getresponse()
    raw_data = response.read()
    encoding = response.info().get_content_charset('utf8')  # JSON Format
    data = json.loads(raw_data.decode(encoding))
    print(json.dumps(data, indent=4))


print(json.dumps(d, indent=2))

login()
dnslb_push()
