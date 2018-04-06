import csv

class Formatter(object):
    """Writes data to a file"""

    @staticmethod
    def writeColumns(writer):
        writer.writeheader()

    @staticmethod
    def writeGames(writer, games):
        for i in range(len(games)):
            writer.writerow(games[i].getData())

    @staticmethod
    def write(games):
        output_file = None
        try:
            output_name = "output.csv"
            output_file = open(output_name, 'w')
        except IOError:
            print("Couldn't open output file. Searching in " + output_name)
            return

        headers = ["Retailer", "Name", "Total Price", "Rank"]
        writer = csv.DictWriter(output_file, fieldnames=headers)
        Formatter.writeColumns(writer)
        Formatter.writeGames(writer, games)


