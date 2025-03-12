import requests
import pandas as pd
import json


APPKEY = "076F672B4DA4B583E60201B37EA4A50A"

    
class LoRaCommunication:

    def __init__(self, server_url):
        self.server_url = server_url
        self.token = None
        self._login()

    
    def _login(self):
        credentials = {
            "username": "admin",
            "password": "admin"
        }
        response = requests.post(self.server_url + "auth/login", json=credentials)
        
        if response.status_code == 200:
            self.token = response.json()['access_token']
        else:
            raise RuntimeError("Não foi possível fazer login")


    def _get_request(self, endpoint):
        return requests.get(self.server_url + endpoint, headers= {"Authorization": f"Bearer {self.token}"}).json()
    

    def _post_request(self, endpoint, data=None):
        return requests.post(self.server_url + endpoint, json = data, headers= {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"})


    def get_tcus(self):
        return self._get_request("tcus")
    

    def post_tcu(self, serial_number, dev_eui, latitude, longitude, elevacao):
        tcus = self.get_tcus()
        try:
            tcu_data = {
                    "tcuId": dev_eui,
                    "nome": serial_number,
                    "latitude": latitude,
                    "longitude": longitude,
                    "elevacao": elevacao,
                    "ativo": True,
                    "validacaoNQuadros": True,
                    "appKey": APPKEY,
            }
            return self._post_request("tcus", tcu_data)
        except Exception as e:
            print(e)


    def get_gateways(self):
        return self._get_request("gateways")

    def post_gateway(self):
        data = {
            "gateway_id": "ac1f09fffe0fce25",
            "ip": "10.50.10.192",
            "name": "Gateway TECSCI",
            "latitude": -20.467005,
            "longitude": -48.022568
        }
        return self._post_request("gateways", data)

    def get_tcu_commands(self):
        return self._get_request("tcu-commands")
    
    def get_device_profile(self):
        return self._get_request("device-profiles")

    def get_plant_info(self):
        return self._get_request("power-plants")
    

    def post_tcu_commands(self, command):
        data = {
            "nome": command[0],
            "codigo": command[1]
        }
        response = self._post_request("tcu-commands", data)
        print(response)


    def create_tcu_dataframe(self, dev_eui):
        data = self._get_request(f"dado-tcu?filter=tcu_fk%20=%20%27{dev_eui}%27&order_by=datetime%20DESC")
        if data:
            df = pd.json_normalize(data)
            df = df[["datetime", "tensao_painel", "tensao_motor", "corrente_motor", "estado_bateria", "temperatura_painel", "posicao_angular", "tcu_fk"]]
            df.to_csv(f"assets/{dev_eui}.csv", index=False)
        else:
            print("Não há dados disponiveis")


    def send_tcu_downlink(self, dev_eui, id):
        try:
            response = self._post_request(f"tcu-commands/{dev_eui}/{id}/downlink")
        except Exception as e:
            print(e)

    def get_last_angle(self, dev_eui):
        data = self._get_request(f"dado-tcu?filter=tcu_fk%20=%20%27{dev_eui}%27&order_by=datetime%20DESC&limit=1")
        angle = pd.json_normalize(data)
        return angle
    

    def create_tcu_dataframe(self, dev_eui):     
        TCU_VARIABLES = ["datetime", "tcuTimestamp", "estado_fk", "posicao_angular", "angulo_calculado", "angulo_target"]
        data = self._get_request(f"dado-tcu?filter=tcu_fk%20=%20%27{dev_eui}%27&order_by=datetime%20DESC")
        if data:
            data = [{key: values[key] for key in TCU_VARIABLES} for values in data]
            return data
        else:
            return "NÃO HÁ DADOS DISPONIVEIS"

SERVER_URL = "http://10.8.0.26:8087/api/v1.0/"
lora = LoRaCommunication(SERVER_URL)
print("a")
