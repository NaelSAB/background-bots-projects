import os
from dotenv import load_dotenv
from scrapeweb import ScrapeWeb
from dataentry import DataEntry

load_dotenv()

GOOGLE_FORM_URL = os.getenv("google_form_url")
PROPERTY_WEBSITE = os.getenv("property_website")


website = ScrapeWeb(PROPERTY_WEBSITE)
website.collect()

data_entry = DataEntry()
data_entry.enter(GOOGLE_FORM_URL, website.links, website.prices, website.addresses)