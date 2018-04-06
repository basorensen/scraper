import random
import requests
import array
from config import Config

class Proxy(object):
    """This is a description of Proxy"""

#    PROXY_LIST = [
#        ("http", "http://50.233.137.32:80"),
#        ("http", "http://50.233.137.39:80"),
#        ("http", "http://47.90.72.227:8088"),
#        ("http", "http://213.136.89.121:80"),
#        ("http", "http://110.77.159.146:3128"),
#        ("http", "http://167.99.48.250:8080"),
#        ("http", "http://218.50.2.102:8080"),
#        ("http", "http://47.75.0.253:3129")
#    ]

    PROXY_LIST = []
    BAD_PROXIES = [] #contains the ip/port of the bad proxies
    LAST_USED_PROXY = ""
    #PROXY_INDEX = 0

    @staticmethod
    def get_next_proxy():
        if len(Proxy.BAD_PROXIES) == len(Proxy.PROXY_LIST):
            raise Exception("All proxies were bad!")
        index = 0
        while True:
            index = random.randint(0, len(Proxy.PROXY_LIST) - 1)
            if Proxy.PROXY_LIST[index][1] not in Proxy.BAD_PROXIES:
                break

        #Proxy.PROXY_INDEX = Proxy.PROXY_INDEX + 1
        #if Proxy.PROXY_INDEX >= len(Proxy.PROXY_LIST):
        #    Proxy.PROXY_INDEX = 0


        prox = {
            Proxy.PROXY_LIST[index][0] : Proxy.PROXY_LIST[index][1]
        }
        Proxy.LAST_USED_PROXY = Proxy.PROXY_LIST[index][1]
        return prox

    @staticmethod
    def mark_bad_proxy():
        Proxy.BAD_PROXIES.append(Proxy.LAST_USED_PROXY)

    @staticmethod
    def get_next_td(html, start_index, i):
        '''Returns the index of the next <td>'''
        offset = 0
        if i > 0:
            offset = offset + len("<td")
        next_td_index = html.index("<td", start_index + offset)
        return next_td_index

    @staticmethod
    def get_td_data(html, td_start_index):
        data_start = html.index(">", td_start_index) + 1
        data_end = html.index("</td>", td_start_index)
        data = html[data_start:data_end]
        return data

    @staticmethod
    def get_row_proxy(html, start_index):
        '''Returns an array of (IP, Port, Protocol)'''
        values = [None, None, None]
        for i in range(0, 7):
            start_index = Proxy.get_next_td(html, start_index, i)
            debug_data = Proxy.get_td_data(html, start_index)
            if i == 0: #IP address
                values[0] = Proxy.get_td_data(html, start_index)
            elif i == 1: #Port
                values[1] = Proxy.get_td_data(html, start_index)
            elif i == 6: #Protocol
                has_https = Proxy.get_td_data(html, start_index)
                values[2] = "https" if has_https == "yes" else "http"

        return values

    @staticmethod
    def load_proxies(use_local):
        html = None
        if use_local:
            proxy_file = open("proxies.html", 'r')
            html =  proxy_file.read()
        else:
            url = "https://free-proxy-list.net/"
            resp = requests.get(url, headers=Config.REQ_HEADERS)
            if resp.status_code != 200:
                raise RuntimeError("server returned error on load proxies")
            html = resp.content


        table_pivot = html.index("<table")
        end_of_column_header_pivot = html.index("</thead>", table_pivot)
        row_pivot = end_of_column_header_pivot
        try:
            while True:
                row_pivot = html.index("<tr>", row_pivot + len("<tr>"))
                proxy_row = Proxy.get_row_proxy(html, row_pivot)
                Proxy.PROXY_LIST.append((proxy_row[2], proxy_row[2] + "://" + proxy_row[0] + ":" + proxy_row[1]))

        except Exception as e:
            print(e.message)
            print("Reached end of proxies")

