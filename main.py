import bestbuy
import amzon
from time import sleep
from game import Game
from formatter import Formatter
from proxy import  Proxy

Proxy.load_proxies(True)

#try:
bestbuy_products = []
page = 1
limit = 1
all_products = []
while len(bestbuy_products) < limit:
    temp_products = bestbuy.get_onsale_products(page)
    bestbuy_products.extend(temp_products)
    page = page + 1

all_products.extend(bestbuy_products)

for i in range(limit):
    bestbuy_product = bestbuy_products[i].getData()

    print "Name:" + bestbuy_product["Name"]
    print "Price: " + str(bestbuy_product["Total Price"])
    try:
       amzon_product = amzon.do_search(bestbuy_product["Name"])
       all_products.append(amzon_product)
    except EnvironmentError as envErr:
        print(envErr.message)
        Proxy.mark_bad_proxy()
        i = i - 1
    sleep(60)

#except Exception as e:
 #   print(e.message)

Formatter.write(all_products)