# Required Libraries
import requests
import json
import os
import dotenv
dotenv.load_dotenv()
from functools import lru_cache
# Base URL
url = 'https://api.imeicheck.net/v1/checks'

token = os.environ.get('API_SANDBOX_TOKEN')

@lru_cache(maxsize=128)
def check_imei(imei:str):
    '''чекает imei, делает запрос на апи, возвращает словарь'''
    # Add necessary headers
    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    }

    # Add body
    body =  json.dumps({
     "deviceId": str(imei),
     "serviceId": 12
    })

    # Execute request
    response = requests.post(url, headers=headers, data=body)

    if str(response.status_code)[0]!='2':
        raise ConnectionError('код ответа не корректный')
    
    return json.loads(response.text)

    
if __name__ == "__main__":
    print(check_imei("356735111052198"))
