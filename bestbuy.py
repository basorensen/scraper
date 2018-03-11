from config import Config
import requests
import simplejson as json


def is_digital_download(name):
    return "[Digital Download" in name

def get_onsale_products():
    apikey = Config.readBestbuyAPIKey()

    url = Config.BESTBUY_URL_BASE + \
          Config.BESTBUY_CATPATH + \
          "?apiKey=" + apikey + \
          "&show=" + ','.join(Config.BESTBUY_RESP_FILTER) + \
          "&format=json"
    resp_raw = requests.get(url)
    resp_parsed = json.loads(resp_raw.content)

    for product in resp_parsed["products"]:
        if is_digital_download(product["name"]): continue

        print "Name:" + product["name"]
        print "Price: " + str(product["salePrice"])

    k = 3
    k = 4
