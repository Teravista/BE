import json
import sys


class Product:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def makeJSON(self):
        dataString = {}
        dataString['name'] = self.name
        dataString['link'] = self.link
        return dataString