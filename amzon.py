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

def get_product_details(page_resp):
    while True:
        sleep(1)
        try:
            doc = html.fromstring(page_resp.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page_resp.status_code != 200:
                raise ValueError('captcha')
            data = {
                'NAME': NAME,
                'SALE_PRICE': SALE_PRICE,
                'CATEGORY': CATEGORY,
                'ORIGINAL_PRICE': ORIGINAL_PRICE,
                'AVAILABILITY': AVAILABILITY
            }

            return data
        except Exception as e:
            print e

def do_search(query):
    escaped_query = urllib.quote(query)
    #resp_html = requests.get(Config.AMAZON_SEARCH_URL_BASE + escaped_query)
    url = "https://www.amazon.com/mn/search/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=The+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&rh=i%3Aaps%2Ck%3AThe+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&fromHash=https%3A%2F%2Fwww.amazon.com%2Fs%2Fref%3Dnb_sb_noss%3Furl%3Dsearch-alias%253Daps%26field-keywords%3DThe%2BLegend%2Bof%2BZelda%253A%2BBreath%2Bof%2Bthe%2BWild%2B-%2BNintendo%2BSwitch&section=BTF&fromApp=gp%2Fsearch&fromPage=results&fromPageConstruction=auisearch&version=2&oqid=1520218159&atfLayout=list&originalQid=1520217955"

    search_resp = requests.get(url, headers=Config.REQ_HEADERS)
    if search_resp.status_code != 200:
        raise RuntimeError("server returned error on search")
    link = get_first_link_in_search_results(search_resp)
    page_resp = requests.get(link, headers=Config.REQ_HEADERS)
    if page_resp.status_code != 200:
        raise RuntimeError("server returned error on product page")
    product_details = get_product_details(page_resp)


