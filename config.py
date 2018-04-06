import random
class Config(object):
    """This is a description of Config"""
    BESTBUY_API_PATH = "../bestbuy_apikey.txt"
    BESTBUY_URL_BASE = "https://api.bestbuy.com/v1/products"
    BESTBUY_MAX_RESULTS = 100
    BESTBUY_RESP_FILTER = ['name', 'salePrice']

    BESTBUY_CATPATH = "(platform=Xbox%20One" \
                      "|(platform=psp" \
                      "|(platform=PlayStation%204" \
                      "|(platform=Nintendo%203DS" \
                      "|(platform=Wii%20U" \
                      ")))))"
    AMAZON_SEARCH_URL_BASE = "https://www.amazon.com/s/ref=nb_sb_noss?field-keywords="
    AMAZON_SEARCH_PIVOT = "s-color-twister-title-link"
    AMAZON_OTHERSELLERS_URL_BASE = "https://www.amazon.com/gp/offer-listing/"
    AMAZON_OTHERSELLERS_URL_ARGS = "/ref=dp_olp_all_mbc?ie=UTF8&f_all=true&f_new=true&sort=taxsip"
    AMAZON_PRODUCTLINK_URL_PIVOT = "/dp/"
    AMAZON_SELLERRANK_PIVOT = "in Video Games"

    AMAZON_OTHERSELLERS_PROPRIETARY_TAG = "alt=\"Amazon.com\""
    AMAZON_OTHERSELLERS_SELLERINFO_PIVOT = "olpSellerName"
    AMAZON_OTHERSELLERS_SELLERINFO_END_PIVOT = "</h3>"
    AMAZON_OTHERSELLERS_OFFERPRICE_PIVOT = "olpOfferPrice"
    AMAZON_OTHERSELLERS_SHIPPINGPRICE_PIVOT = "olpShippingPrice"
    AMAZON_OTHERSELLERS_TAXPRICE_PIVOT = "olpEstimatedTaxText"

    REQ_HEADERS_LIST = [
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        },
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        },
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
        },
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
        },
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36"
        }
    ]

    @staticmethod
    def get_next_header():
        index = random.randint(0, len(Config.REQ_HEADERS_LIST) - 1)
        head = Config.REQ_HEADERS_LIST[index]
        return head

    @staticmethod
    def readBestbuyAPIKey():
        file = open(Config.BESTBUY_API_PATH, 'r')
        key = file.read().strip()
        return key