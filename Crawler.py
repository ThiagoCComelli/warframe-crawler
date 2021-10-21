import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from Mod import Mod

class Crawler:
    modRepositoryBaseLink = "https://warframe.fandom.com/wiki/Category:Mods?from="

    def __init__(self):
        self.__modsNames = []
    
    def getModsNames(self):
        return self.__mods
    
    def newModsNames(self,name):
        if("Category" in name):
            return
        self.__modsNames.append(name)
    
    def requestModsNames(self):
        for i in range(65,66):
            print(f"{i-65}/{91-65}")
            response = requests.get(Crawler.modRepositoryBaseLink+chr(i))
            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all("li", class_="category-page__member")

            for i in items:
                modName = i.find("a", class_="category-page__member-link").text
                self.newModsNames(modName)
    
    def startThreadFunction(self,item):
        print(f"Coletando: {item}")

        # .start(arg)
        # True || False
        # arg= True (Will download mod png and save) 
        # WARNING all files weight is around in 201mb
        Mod(item[1]).start(False)

    def start(self):
        print("Iniciando coleta de nomes")
        self.requestModsNames()

        print("Iniciando coleta dos status de cada mod")
        with ThreadPoolExecutor(max_workers=9) as pool:
            for i in enumerate(self.__modsNames):
                pool.submit(self.startThreadFunction,i)

        # for index, i in enumerate(self.__modsNames):
        #     print(f"{index}/{len(self.__modsNames)}")
        #     Mod(i).start()
        

        