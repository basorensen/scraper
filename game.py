class Game(object):

    def __init__(self, retailer, name, price, rank):
        self.data = {
            'Retailer' : retailer,
            'Name' : name,
            'Total Price': price,
            'Rank' : rank
        }

    def getData(self):
        return self.data