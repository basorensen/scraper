class Proxy(object):
    """This is a description of Proxy"""

    PROXY_LIST = [
        ("http", "http://50.233.137.32:80"),
        ("http", "http://50.233.137.39:80"),
        ("http", "http://47.90.72.227:8088"),
        ("http", "http://213.136.89.121:80"),
        ("http", "http://110.77.159.146:3128"),
        ("http", "http://167.99.48.250:8080"),
        ("http", "http://218.50.2.102:8080"),
        ("http", "http://47.75.0.253:3129")
    ]

    PROXY_INDEX = 0

    @staticmethod
    def get_next_proxy():
        Proxy.PROXY_INDEX = Proxy.PROXY_INDEX + 1
        if Proxy.PROXY_INDEX >= len(Proxy.PROXY_LIST):
            Proxy.PROXY_INDEX = 0
        prox = {
            Proxy.PROXY_LIST[Proxy.PROXY_INDEX][0] : Proxy.PROXY_LIST[Proxy.PROXY_INDEX][1]
        }
        return prox