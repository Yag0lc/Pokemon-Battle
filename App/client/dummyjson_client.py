import requests

class DummyJsonClient:
    def __init__(self):
        self._cache = {}

    def get_product(self, id):
        if id in self._cache:
            return self._cache[id]

        url = f"https://dummyjson.com/products/{id}"

        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        self._cache[id] = data
        return data

product_client = DummyJsonClient()