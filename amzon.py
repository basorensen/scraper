import requests
import urllib
from config import Config

def get_first_link_in_search_results(html):
    pivot_index = html.index(Config.AMAZON_SEARCH_PIVOT)
    href = "href=\""
    link_start = html.index(href, pivot_index) + len(href)
    link_end = html.index("\"", link_start)
    link = html[link_start:link_end]
    return link

def do_search(query):
    escaped_query = urllib.quote(query)
    #resp_html = requests.get(Config.AMAZON_SEARCH_URL_BASE + escaped_query)
    url = "https://www.amazon.com/mn/search/ajax/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=The+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&rh=i%3Aaps%2Ck%3AThe+Legend+of+Zelda%3A+Breath+of+the+Wild+-+Nintendo+Switch&fromHash=https%3A%2F%2Fwww.amazon.com%2Fs%2Fref%3Dnb_sb_noss%3Furl%3Dsearch-alias%253Daps%26field-keywords%3DThe%2BLegend%2Bof%2BZelda%253A%2BBreath%2Bof%2Bthe%2BWild%2B-%2BNintendo%2BSwitch&section=BTF&fromApp=gp%2Fsearch&fromPage=results&fromPageConstruction=auisearch&version=2&oqid=1520218159&atfLayout=list&originalQid=1520217955"

    resp_html = requests.get(url, headers=Config.REQ_HEADERS)
    link = get_first_link_in_search_results(resp_html)
