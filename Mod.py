import requests
import json
from bs4 import BeautifulSoup

class Mod:
    modBaseLink = "https://warframe.fandom.com/wiki/"

    def __init__(self, name):
        self.__name = name
        self.__type = None
        self.__polarity = None
        self.__rarity = None
        self.__tradingTax = None
        self.__maxRank = None
        self.__baseCapacityCost = None
        self.__modObject = None
        self.__url = Mod.modBaseLink + name
    
    def createJson(self):
        self.__modObject = {
            "name": self.__name,
            "type": self.__type,
            "polarity": self.__polarity,
            "rarity": self.__rarity,
            "tradingTax": self.__tradingTax,
            "maxRank": self.__maxRank,
            "baseCapacityCost": self.__baseCapacityCost,
        }

        with open(f"mods/{self.__name}.json", "w+") as file:
            json.dump(self.__modObject, file, indent=3)

    def requestModStats(self):
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')

        itemRootAllStats = soup.find_all("section", class_="pi-item pi-group pi-border-color pi-collapse pi-collapse-open")

        itemStats = itemRootAllStats[1].find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color")

        self.__type = itemStats[0].find("div").text.strip()
        self.__polarity = itemStats[1].find("div").text.strip()
        self.__rarity = itemStats[2].find("div").text.strip()
        self.__tradingTax = itemStats[3].find("div").text.strip()
        self.__maxRank = itemStats[4].find("div").text.strip()
        self.__baseCapacityCost = itemStats[5].find("div").text.strip()
    
    def requestModImage(self):
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')

        itemImageDiv = soup.find("a", class_="image image-thumbnail")
        itemImageLink = itemImageDiv.attrs["href"]

        image = requests.get(itemImageLink)

        with open(f"mods/{self.__name}.png", "wb") as file:
            file.write(image.content)

    def start(self,image=False):
        self.requestModStats()
        self.createJson()
        self.requestModImage() if image else None

    