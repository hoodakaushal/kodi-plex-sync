import json

import requests


# noinspection PyPep8Naming
from logger import logger


class KodiRPC:
    def __init__(self, serverUrl="http://localhost:8080"):
        self.server = serverUrl + "/jsonrpc"

    def rpc(self, method: str = "JSONRPC.Introspect", params: dict = None, requestId=1):
        logger.debug("RPC {} {}".format(method, params))
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

    def getEpisodes(self):
        params = {
            "properties": ["playcount", "file"]
        }
        return self.rpc("VideoLibrary.GetEpisodes", params)["episodes"]

    def markEpisodeWatched(self, episode):
        if episode["playcount"] == 0:
            params = {
                "episodeid": episode["episodeid"],
                "playcount": 1
            }
            return self.rpc("VideoLibrary.SetEpisodeDetails", params)

    def markEpisodeUnwatched(self, episode):
        params = {
            "episodeid": episode["episodeid"],
            "playcount": 0
        }
        return self.rpc("VideoLibrary.SetEpisodeDetails", params)

    def getMovies(self):
        params = {
            "properties": ["playcount", "file"]
        }
        return self.rpc("VideoLibrary.GetMovies", params)["movies"]

    def markMovieWatched(self, movie):
        if movie["playcount"] == 0:
            params = {
                "movieid": movie["movieid"],
                "playcount": 1
            }
            return self.rpc("VideoLibrary.SetMovieDetails", params)

    def markMovieUnwatched(self, movie):
        params = {
            "movieid": movie["movieid"],
            "playcount": 0
        }
        return self.rpc("VideoLibrary.SetMovieDetails", params)


if __name__ == "__main__":
    print(json.dumps(KodiRPC().getEpisodes(), indent=4))
