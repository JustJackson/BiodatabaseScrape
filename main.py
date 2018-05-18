from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import boto3
import matplotlib.pyplot as plt
from tqdm import tqdm

df = pd.DataFrame()
master_text = []

for i in range(0, 8500, 100):
    req_query = f'https://wwwdev.ebi.ac.uk/biomodels/search?query=*%3A*&offset={i}&numResults=100&sort=relevance-desc'
    directory_listing = requests.get(req_query)
    outer_soup = BeautifulSoup(directory_listing.content, "html.parser")
    for link in tqdm(outer_soup.find_all('a', href=True), desc=f'On Group {i}'):
        if re.match(r'^(\/biomodels\/MODEL)', link.attrs['href']):
            model_query = f'https://wwwdev.ebi.ac.uk{link.attrs["href"]}'
            model_actual = f'https://wwwdev.ebi.ac.uk/biomodels/model/download/{(link.attrs["href"])[10:]}.2?filename = {(link.attrs["href"])[10:]}'
            model_page = requests.get(model_query)
            inner_soup = BeautifulSoup(model_page.content, "html.parser")
            div = inner_soup.find(id="description")
            try:
                with open("BioModelsDatabase.txt", 'a') as output_file:
                    output_file.write(div.text.replace('\n', ''))
            except AttributeError as e:
                continue

stopword_list = ["the", "of", "model", "and", "to", "from", "by", "et", "a", "is", "for	", "with",
                 "metabolic", "been", "information", "Human", "GDC", "or", "BioModels", "this", "have", "encoded",
                 "copyright", "on", "more", "was", "under", "all", "Database", "possible", "related	", "please",
                 "extent", "public", "cite", "use:", "rights", "dedicated", "domain", "refer", "worldwide.", "law,",
                 "neighbouring","Please", "Public", "Domain", "CC0	", "Dedication", "A", "human", "metabolism", "Syst",
                 "Chelliah", "identified", "at", "hosted", "genome-scale", "has", "automaticaly", "using", "Metabolic",
                 "genome", "M.,", "through", "where", "via", "generated", "pathway", "accessed", "43", "modeling",
                 "release"]
