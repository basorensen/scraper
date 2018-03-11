class Config(object):
    """This is a description of Config"""
    BESTBUY_URL_BASE = "https://api.bestbuy.com/v1/products"
    BESTBUY_MAX_RESULTS = 100
    BESTBUY_RESP_FILTER = ['name', 'salePrice']

    BESTBUY_CATPATH = "(onSale=true" \
                      "&(platform=Xbox%20One" \
                      "|(platform=psp" \
                      "|(platform=PlayStation%204" \
                      "|(platform=Nintendo%203DS" \
                      "|(platform=Wii%20U" \
                      "))))))"
    AMAZON_SEARCH_URL_BASE = "https://www.amazon.com/s/ref=nb_sb_noss?field-keywords="
    AMAZON_SEARCH_PIVOT = "s-color-twister-title-link"

    REQ_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "en-US,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }