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

    REQ_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "en-US,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }

    @staticmethod
    def readBestbuyAPIKey():
        file = open(Config.BESTBUY_API_PATH, 'r')
        key = file.read().strip()
        return key