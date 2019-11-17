import json

import requests


# noinspection PyPep8Naming
class KodiRPC:
    def __init__(self, serverUrl="http://localhost:8080"):
        self.server = serverUrl + "/jsonrpc"

    def rpc(self, method: str = "JSONRPC.Introspect", params: dict = None, requestId=1):
        if params is None:
            params = {}
        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": requestId
        }
        resp = requests.post(self.server, json=data)
        if resp.status_code // 100 != 2:
            raise Exception("Request failed with response code {}, response {}".format(resp.status_code, resp.text))
        resp = resp.json()
        assert resp['id'] == requestId
        if 'error' in resp:
            raise Exception(str(resp['error']))
        return resp['result']

    def getDocs(self):
        return self.rpc()


if __name__ == "__main__":
    print(json.dumps(KodiRPC().getDocs(), indent=4))
