from config import Config
import requests
import simplejson as json


def is_digital_download(name):
    return "[Digital" in name

def get_onsale_products(page):
    apikey = Config.readBestbuyAPIKey()

    url = Config.BESTBUY_URL_BASE + \
          Config.BESTBUY_CATPATH + \
          "?apiKey=" + apikey + \
          "&show=" + ','.join(Config.BESTBUY_RESP_FILTER) + \
          "&format=json&page=" + str(page)
    resp_raw = requests.get(url)
    resp_parsed = json.loads(resp_raw.content)

    real_products = []
    for product in resp_parsed["products"]:
        if is_digital_download(product["name"]): continue

        real_products.append(product)

    return real_products