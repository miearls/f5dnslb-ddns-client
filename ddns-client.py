import requests
import json
import yaml
import time
import logging

config = open("setup_config.yaml", "r")
configInput = yaml.load(config, Loader=yaml.FullLoader)
f5saasUsername = configInput['f5cs_username']
f5saasPassword = configInput['f5cs_password']
my_service_instance_name = configInput['service_instance_name']
my_lbr_name = configInput['lbr_name']
my_lbr_aliases = configInput['lbr_aliases']
my_virtual_servers = configInput['virtual_servers']
my_pools = configInput['pools']
my_monitors = configInput['monitors']
checkInterval = configInput['checkInterval']
my_query_servers = configInput['ip_query']
newIPAddress = "144.144.144.144"
#subscription_id = F5CS.self.subscription_id

logger = logging.getLogger(__name__)
# Create handlers
f_handler = logging.FileHandler('error.log')
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

class F5CS:
    def __init__(self):
        self.type = 'f5_cloud_services'
        # Primary key
        self.id = f5saasUsername
        # Attribute
        self.host = 'api.cloudservices.f5.com'
        self.username = f5saasUsername
        self.password = f5saasPassword
        self.session = None
        self.access_token = None
        self.refresh_token = None
        self.primary_account_id = None
        self.catalog_id = "c-aaQnOrPjGu"
        self.service_type = "gslb"
        self.subscription_id = None
        self.myip = ""

    def _ipquery(self):
        r = requests.get(my_query_servers, timeout=3)
        self.myip = r.text.strip()
        logger.debug("Finding the external IP and adding it to the ip object")
        print("finding the external IP and adding it to an object")
        return self.myip


    def get_token(self):
        self.session = requests.session()
        url = "https://" + self.host + "/v1/svc-auth/login"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "username": self.username,
            "password": self.password
        }
        r = self.session.post(
            url,
            headers=headers,
            data=str(data).replace("\'", "\""),
            verify=True
        )
        if r.status_code != requests.codes.ok:
            logger.warning("Error on getting the user tokens", r.status_code)
            print("error on the status code")
            raise
        else:
            self.access_token = r.json()["access_token"]
            self.refresh_token = r.json()["refresh_token"]
            print("got the token an refresh token", self.access_token, self.refresh_token)

    def _get(self, path, parameters=None):
        if parameters and len(parameters) > 0:
            uri = path + "?" + "&".join(parameters)
            ## print("first one " + uri)
        else:
            uri = path
            ## print("second print ", uri)
        url = "https://" + self.host + uri
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        r = self.session.get (
            url,
            headers=headers,
            verify=True
        )
        print("_get URL", url)
        print(r.json())
        return r.json()

    def _post(self, path, parameters=None):
        uri = path
        url = "https://" + self.host + uri
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        r = self.session.post(
            url,
            headers=headers,
            verify=True
        )
        if r.text == " ":
            return {}
        else:
            print("getting the post url", url)
            print(r.json())
            return r.json()

    def get_account_user(self):
        path = "/v1/svc-account/user"
        parameters = []
        self.primary_account_id = self._get(path, parameters)["primary_account_id"]
        account_id = self.primary_account_id
        print("getting the account use info", path, self.primary_account_id)

    def get_subscription(self):
        path = "/v1/svc-subscription/subscriptions"
        parameters = [
            'catalog_id=' + self.catalog_id,
            'account_id=' + self.primary_account_id,
            'service_type=' + self.service_type,
        ]
        print("pulling subscriptions", path, parameters)
        ##print(parameters)
        return self._get(path, parameters)

    def mypost(self, path, payload):
        url = "https://" + self.host + path
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        payload = json.dumps(payload)
        r = self.session.post(
            url,
            data=payload,
            headers=headers
        )
        if r.status_code not in (200, 201, 202, 204):
            logger.warning("Error on posting update", r.status_code)
            print(r.status_code)
        if r.text == '':
            return {}
        else:
            self.subscription_id = r.json()["subscription_id"]
            self._activate(self.subscription_id)
            print("push data from mypost", url, self.subscription_id)
            print(r.json())
            return self.subscription_id

    def _update(self, path, payload):
        url = "https://" + self.host + path
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        payload = json.dumps(payload)
        r = self.session.put(
            url,
            data=payload,
            headers=headers
        )
        print("push _update, calling update gslb instance", url, self.subscription_id)
        print(r.json())
        return self.subscription_id
        self.updateGSLBInstance(self.subscription_id)


    def _activate(self, subscription_id):
        path = "/v1/svc-subscription/subscriptions/" + self.subscription_id + "/activate"
        return self._post(path)
        self.status = r.json()["status"]
        self.subscription_id = r.json["subscription_id"]
        print("_activating the instance", path, self.status)
        print(self.status)

    def createGSLBInstance(self):
        path = "/v1/svc-subscription/subscriptions"
        payload = {
            "account_id": self.primary_account_id,
            "catalog_id": "c-aaQnOrPjGu",
            "service_type": "gslb",
            "service_instance_name": my_service_instance_name,
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
                            "persistence_ttl": 3600,
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
                            "address": newIPAddress,
                            "display_name": my_virtual_servers,
                            "monitor": my_monitors,
                            "port": 80,
                            "virtual_server_type": "cloud"
                        }
                    }, "zone": my_service_instance_name
                }
            }
        }
        print("Creating a new gslb instance", path, payload)
        return self.mypost(path, payload)

    def updateGSLBInstance(self):
        F5CS._ipquery(self)
        path = "/v1/svc-subscription/subscriptions/" + self.subscription_id
        payload = {
            "account_id": self.primary_account_id,
            "catalog_id": "c-aaQnOrPjGu",
            "service_type": "gslb",
            "service_instance_name": my_service_instance_name,
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
                            "persistence_ttl": 3600,
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
                            "address": self.myip,
                            "display_name": my_virtual_servers,
                            "monitor": my_monitors,
                            "port": 80,
                            "virtual_server_type": "cloud"
                        }
                    }, "zone": my_service_instance_name
                }
            }
        }
        print("Updating gslb instance sending to _update", path, payload)
        return self._update(path, payload)

ddns = F5CS()

ddns.get_token()
ddns.get_account_user()
if ddns.subscription_id == None:
    ddns.createGSLBInstance()
else:
    ddns.updateGSLBInstance()
while True:
    ddns.updateGSLBInstance()
    logger.info("Sh... Sleeping while you work")
    time.sleep(checkInterval)
