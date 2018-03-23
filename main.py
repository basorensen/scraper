import bestbuy
import amzon

try:
    #bestbuy.get_onsale_products()
    title = "Super Mario Odyssey - Nintendo Switch"
    amzon.do_search(title)
except Exception as e:
    print(e.message)