import bestbuy
import amzon
from time import sleep
#try:
bestbuy_products = []
page = 1
while len(bestbuy_products) < 10:
    bestbuy_products = bestbuy.get_onsale_products(page)
    page = page + 1

for i in range(10):
    sleep(1)
    product = bestbuy_products[i]
    print "Name:" + product["name"]
    print "Price: " + str(product["salePrice"])
    amzon.do_search(product["name"])

#except Exception as e:
 #   print(e.message)
