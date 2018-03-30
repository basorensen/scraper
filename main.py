import bestbuy
import amzon
from time import sleep
#try:
bestbuy_products = []
page = 1
limit = 20
while len(bestbuy_products) < limit:
    temp_products = bestbuy.get_onsale_products(page)
    bestbuy_products.extend(temp_products)
    page = page + 1

for i in range(limit):
    sleep(5)
    product = bestbuy_products[i]
    print "Name:" + product["name"]
    print "Price: " + str(product["salePrice"])
    amzon.do_search(product["name"])

#except Exception as e:
 #   print(e.message)
