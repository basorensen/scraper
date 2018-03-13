import bestbuy
import amzon

try:
    #bestbuy.get_onsale_products()
    amzon.do_search("The Legend of Zelda: Breath of the Wild - Nintendo Switch")
except Exception as e:
    print(e.message)