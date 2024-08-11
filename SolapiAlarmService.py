# solapi_alarm_service.py

import time
import datetime
import uuid
import hmac
import hashlib
import requests
import platform

class SolapiAlarmService:
    def __init__(self, api_key, api_secret, sender_phone):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sender_phone = sender_phone
        self.protocol = 'https'
        self.domain = 'api.solapi.com'
        self.prefix = ''

    def unique_id(self):
        return str(uuid.uuid1().hex)

    def get_iso_datetime(self):
        utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
        utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
        return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

    def get_signature(self, msg):
        return hmac.new(self.api_secret.encode(), msg.encode(), hashlib.sha256).hexdigest()

    def get_headers(self):
        date = self.get_iso_datetime()
        salt = self.unique_id()
        combined_string = date + salt

        return {
            'Authorization': 'HMAC-SHA256 ApiKey=' + self.api_key + ', Date=' + date + ', salt=' + salt + ', signature=' +
                            self.get_signature(combined_string),
            'Content-Type': 'application/json; charset=utf-8'
        }
    
    def get_url(self, path):
        url = f'{self.protocol}://{self.domain}'
        if self.prefix != '':
            url = url + self.prefix
        url = url + path
        return url

    def send_many(self, parameter):
        parameter['agent'] = {
            'sdkVersion': 'python/4.2.0',
            'osPlatform': platform.platform() + " | " + platform.python_version()
        }

        return requests.post(self.get_url('/messages/v4/send-many'), headers=self.get_headers(), json=parameter)