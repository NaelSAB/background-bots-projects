from bs4 import BeautifulSoup
import requests


class ScrapeWeb:
    def __init__(self, url):
        self.response = requests.get(url)
        self.response.raise_for_status()
        self.data = self.response.text
        self.soup = BeautifulSoup(self.data, "html.parser")
        self.links = []
        self.prices = []
        self.addresses = []

    def collect(self):
        links_elements = self.soup.select("a.StyledPropertyCardDataArea-anchor")
        self.links = [link["href"] for link in links_elements]
        self.addresses = [address.text.strip() for address in links_elements]
        prices_elements = self.soup.select("span.PropertyCardWrapper__StyledPriceLine")
        self.prices = [a.text.split("+")[0].split("/")[0] for a in prices_elements]
        # print(len(self.links))
        # print(len(self.addresses))
        # print(len(self.prices))
