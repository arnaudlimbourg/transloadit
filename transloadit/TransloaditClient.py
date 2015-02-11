import requests
import hmac
import hashlib
import json

from datetime import datetime, timedelta


BASE_API = "https://api2.transloadit.com"


class TransloaditClient(object):
    params = {}

    def __init__(self, key, secret, api=None):
        self.auth_key = key
        self.secret = secret
        if api:
            self.api = api
        else:
            self.api = BASE_API

    def _signature(self, params):
        return hmac.new(self.secret, params, hashlib.sha1).hexdigest()

    def _send_post_request(self, endpoint, template_id=None, files=None,
                           assembly_steps=None):
        params = self.params

        params.update({
            'auth': {
                'key': self.auth_key,
                'expires': (datetime.now() +
                            timedelta(minutes=30)).strftime('%Y/%m/%d %H:%M:%S')
            }
        })

        if template_id is not None and assembly_steps is not None:
            raise ValueError("template_id and assembly_steps are mutually exclusive")

        if template_id is not None:
            params["template_id"] = template_id

        if assembly_steps is not None:
            params["steps"] = assembly_steps

        params = json.dumps(params)

        signature = self._signature(params)

        payload = {
            'params': params,
            'signature': signature
        }

        response = requests.post(endpoint, data=payload, files=files)
        return response

    def upload(self, file_descriptor, assembly_steps=None, template_id=None, params=None):
        """Upload a file to transloadit

        You must give it an file descriptor like open("file", "rb")
        Optionally you can provide assembly steps as a dictionnary. Steps should
        follow transloadit documentation, there are not validated in any way.
        Another option is to provide a template_id as per documentation

        Will raise a ValueError on failure or return a code
        corresponding to a success status status. Mapping can be found
        at https://transloadit.com/docs/api-docs#status-codes

        usage:
            client = TransloaditClient(KEY, SECRET)
            file = open(FILE)
            steps = {
             "resize_to_250": {
                    "robot": "/image/resize",
                    "width": 250,
                    "height": 250
                },
            }

            status = client.upload(file, assembly_steps=steps)
            status = client.upload(file, template_id=TEMPLATE_ID)
        """

        endpoint = '{0}/{1}'.format(self.api, 'assemblies')

        if params is not None:
            self.params.update(params)

        files = {'file': file_descriptor}
        response = self._send_post_request(endpoint, files=files,
                                           assembly_steps=assembly_steps,
                                           template_id=template_id)

        try:
            data = response.json()
        except ValueError:
            raise ValueError("error communicating with transloadit API {0}".format(
                response.status_code)
            )

        if "error" in data:
            raise ValueError("upload failed {0}".format(data))

        if "ok" in data:
            return data
