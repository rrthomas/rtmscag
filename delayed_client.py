# Company Info, Tools for using the Companies House API, by Martin Keegan
#
# To the extent (if any) permissible by law, Copyright (C) 2022  Martin Keegan
#
# This programme is free software; you may redistribute and/or modify it under
# the terms of the Apache Software Licence v2.0.

import time
import requests
from requests.auth import HTTPBasicAuth

class DelayedClient:
    def __init__(self, api_key):
        self.delay = 0.501
        self.auth = HTTPBasicAuth(api_key, "")

    def get(self, url, **kwargs):
        time.sleep(self.delay)
        kwargs["auth"] = self.auth
        return requests.get(url, **kwargs)

    def iter_results(self, url, common_params, start_index):
        step = 20
        while True:
            params = dict(common_params)
            params.update({"start_index": start_index})

            response = self.get(url, params=params)
            status = response.status_code
            if status == 500:
                break
            assert status == 200, status
            for i in response.json()["items"]:
                yield start_index, i
            start_index += step
