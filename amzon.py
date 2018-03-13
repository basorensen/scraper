import requests
import urllib
from config import Config
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

def extract_asin(url):
    start_index = url.index(Config.AMAZON_PRODUCTLINK_URL_PIVOT) + len(Config.AMAZON_PRODUCTLINK_URL_PIVOT)
    end_index = url.index("/", start_index)
    asin = url[start_index:end_index]
    return asin

def get_bestseller_rank(resp):
    html = resp.content
    pivot = html.index(Config.AMAZON_SELLERRANK_PIVOT)
    numb_start = html.rfind("#", 0, pivot) + 1
    numb_end = html.find(" ", numb_start)
    rank = html[numb_start:numb_end]
    return rank

def do_search(query):
    escaped_query = urllib.quote(query)
    #resp_html = requests.get(Config.AMAZON_SEARCH_URL_BASE + escaped_query)
    url = "https://www.amazon.com/mn/search/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=The+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&rh=i%3Aaps%2Ck%3AThe+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&fromHash=https%3A%2F%2Fwww.amazon.com%2Fs%2Fref%3Dnb_sb_noss%3Furl%3Dsearch-alias%253Daps%26field-keywords%3DThe%2BLegend%2Bof%2BZelda%253A%2BBreath%2Bof%2Bthe%2BWild%2B-%2BNintendo%2BSwitch&section=BTF&fromApp=gp%2Fsearch&fromPage=results&fromPageConstruction=auisearch&version=2&oqid=1520218159&atfLayout=list&originalQid=1520217955"

    search_resp = requests.get(url, headers=Config.REQ_HEADERS)
    if search_resp.status_code != 200:
        raise RuntimeError("server returned error on search")
    link = get_first_link_in_search_results(search_resp)

    #get lowest price
    asin = extract_asin(link)
    othersellers_url = make_othersellers_url(asin)
    othersellers_resp = requests.get(othersellers_url, headers=Config.REQ_HEADERS)
    if othersellers_resp.status_code != 200:
        raise RuntimeError("server returned error on othersellers page")

    #get seller's rank
    product_resp = requests.get(link, headers=Config.REQ_HEADERS)
    if product_resp.status_code != 200:
        raise RuntimeError("server returned error on product page")
    rank = get_bestseller_rank(product_resp)


    #product_details = get_product_details(page_resp)


