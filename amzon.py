import requests
import urllib
from config import Config
from proxy import Proxy
from time import sleep
from lxml import html

class LinkResult(object):
    """Contains the link and the end index."""
    def __init__(self, link, end_index):
        self.link = link
        self.end_index = end_index


def find_link(html, start_index):
    pivot_index = html.index(Config.AMAZON_SEARCH_PIVOT, start_index)
    href = "href=\""
    link_start = html.index(href, pivot_index) + len(href)
    link_end = html.index("\"", link_start)
    link = html[link_start:link_end]
    result = LinkResult(link, link_end)
    return result

def get_first_link_in_search_results(resp):
    html = resp.content
    link_result = find_link(html, 0)
    if "picasso" in link_result.link: #skip advertisement
        link_result = find_link(html, link_result.end_index + 1)

    return link_result.link

def make_othersellers_url(asin):
    return Config.AMAZON_OTHERSELLERS_URL_BASE + asin + Config.AMAZON_OTHERSELLERS_URL_ARGS

def parse_price(html, dollar_index):
    index = dollar_index + 1
    numstr = ""
    while html[index].isdigit() or html[index] == ".":
        numstr = numstr + html[index]
        index = index + 1

    return float(numstr)

def is_amazon_seller(html):
    seller_index = html.index(Config.AMAZON_OTHERSELLERS_SELLERINFO_PIVOT)
    seller_end = html.index(Config.AMAZON_OTHERSELLERS_SELLERINFO_END_PIVOT, seller_index)
    try:
        amazon_index = html.index(Config.AMAZON_OTHERSELLERS_PROPRIETARY_TAG, seller_index)
        if amazon_index < seller_end:
            return True
        else:
            return False
    except:
        return False


def get_price(html, pivot_index):
    dollar_index = html.index("$", pivot_index)
    ending_index = html.index("</span>", pivot_index)
    if dollar_index > ending_index:
        return 0
    return parse_price(html, dollar_index)

def get_othersellers_lowest_prices(resp):

    html = resp.content
    if is_amazon_seller(html):
        return [-1, -1, -1]

    prices = [0, 0, 0] #main, shipping, tax

    offer_start = html.index("a-spacing-mini olpOffer")
    offer_end = html.index("</p>", offer_start)

    try:
        mainprice_index = html.index(Config.AMAZON_OTHERSELLERS_OFFERPRICE_PIVOT, offer_start)
        if mainprice_index > offer_end:
            print("mainprice_index wastoo big.")
            return prices
        prices[0] = get_price(html, mainprice_index)
    except Exception as e:
        print("Error in mainprice_index: " + e.message)
        
    try:
        shippingprice_index = html.index(Config.AMAZON_OTHERSELLERS_SHIPPINGPRICE_PIVOT, offer_start)
        if shippingprice_index < offer_end:
            prices[1] = get_price(html, shippingprice_index)
    except Exception as e:
        print("Error in shippingprice_index: " + e.message)


    try:
        taxprice_index = html.index(Config.AMAZON_OTHERSELLERS_TAXPRICE_PIVOT, offer_start)
        if taxprice_index < offer_end:
            prices[2] = get_price(html, taxprice_index)
    except Exception as e:
        print("Error in taxprice_index: " + e.message)


    return prices

def extract_asin(url):
    print("ASIN url: " + url)
    try:
        start_index = url.index(Config.AMAZON_PRODUCTLINK_URL_PIVOT) + len(Config.AMAZON_PRODUCTLINK_URL_PIVOT)
        end_index = url.index("/", start_index)
        asin = url[start_index:end_index]
        return asin
    except:
        print("Error in extract_asin")
        return ""

def get_bestseller_rank(resp):
    html = resp.content
    pivot = html.index(Config.AMAZON_SELLERRANK_PIVOT)
    numb_start = html.rfind("#", 0, pivot) + 1
    numb_end = html.find(" ", numb_start)
    rank = html[numb_start:numb_end]
    return rank

def do_search(query):
    escaped_query = urllib.quote(query.encode('utf8'))
    url = Config.AMAZON_SEARCH_URL_BASE + escaped_query
    print("Search URL: " + url)
    #url = "https://www.amazon.com/mn/search/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=The+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&rh=i%3Aaps%2Ck%3AThe+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&fromHash=https%3A%2F%2Fwww.amazon.com%2Fs%2Fref%3Dnb_sb_noss%3Furl%3Dsearch-alias%253Daps%26field-keywords%3DThe%2BLegend%2Bof%2BZelda%253A%2BBreath%2Bof%2Bthe%2BWild%2B-%2BNintendo%2BSwitch&section=BTF&fromApp=gp%2Fsearch&fromPage=results&fromPageConstruction=auisearch&version=2&oqid=1520218159&atfLayout=list&originalQid=1520217955"

    search_resp = requests.get(url, headers=Config.REQ_HEADERS, proxies=Proxy.get_next_proxy())
    if search_resp.status_code != 200:
        raise RuntimeError("server returned error on search")
    link = get_first_link_in_search_results(search_resp)

    #get lowest price
    asin = extract_asin(link)
    print("ASIN is: " + asin)
    othersellers_url = make_othersellers_url(asin)
    print("Amazon URL: " + othersellers_url)
    othersellers_resp = requests.get(othersellers_url, headers=Config.REQ_HEADERS, proxies=Proxy.get_next_proxy())
    if othersellers_resp.status_code != 200:
        raise RuntimeError("server returned error on othersellers page")
    prices = get_othersellers_lowest_prices(othersellers_resp)
    if prices[0] == -1:
        print("Amazon was seller, didn't calculate price.")
    else:
        print("Main price: " + str(prices[0]))
        print("Shipping price: " + str(prices[1]))
        print("Tax price: " + str(prices[2]))
        print("Total price: " + str(prices[0] + prices[1] + prices[2]))


    #get seller's rank
    product_resp = requests.get(link, headers=Config.REQ_HEADERS, proxies=Proxy.get_next_proxy())
    if product_resp.status_code != 200:
        raise RuntimeError("server returned error on product page")
    try:
        rank = get_bestseller_rank(product_resp)
        print("Rank is: " + rank)
    except:
        print("Rank was not found.")

    #product_details = get_product_details(page_resp)


