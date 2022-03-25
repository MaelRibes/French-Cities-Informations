import requests
from bs4 import BeautifulSoup
import pandas as pd
import unidecode
import re
from tqdm import tqdm


def create_soup_from(departement):
    site = requests.get('https://www.annuaire-mairie.fr/departement-' + departement + '.html').text
    soup = BeautifulSoup(site, "html.parser")
    if departement == "Paris":
        soup = "Paris"
    return soup


def create_soup():
    global departement
    departement = input("Entrez un département : ")
    site = requests.get('https://www.annuaire-mairie.fr/departement-' + departement + '.html').text
    soup = BeautifulSoup(site, "html.parser")
    return soup


def create_soup_departements():
    site = requests.get('https://www.annuaire-mairie.fr').text
    soup = BeautifulSoup(site, "html.parser")
    return soup


def get_tableau_communes(soup):
    if soup == "Paris":
        communes = "Paris"
    else:
        commune_content = soup.find(id="les_commune_content")
        tbl_communes = commune_content.find_next(class_="tblmaire")
        communes = tbl_communes.find_next('tbody').find_all('tr')

    return communes


def get_list_departement():
    list_dep = []
    soup = create_soup_departements()
    map = soup.find(id="usemap")
    areas = map.find_all("area")
    for a in areas:
        txt = a["alt"]
        ascii = unidecode.unidecode(txt)
        x = ascii.replace("'","-")
        ascii = x
        if ascii == "Bouche-du-Rhone":
            ascii = "Bouches-du-Rhone"
        if ascii == "Essone":
            ascii = "Essonne"
        list_dep.append(ascii)
    return list_dep


def info_commune(balise):
    if balise == "Paris":
        data = {'commune': 'Paris (capitale)', 'code_INSEE': '75056', 'code_postal': 75000, 'population': 2165423, 'superficie (km²)': 105.4, 'densité (hab./km²)': 20544.8}
    else:
        cpt = 0
        data = {'commune': '', 'code_INSEE': 0, 'code_postal': 0, 'population': 0, 'superficie (km²)': 0.0, 'densité (hab./km²)': 0.0}
        for td in balise:
            x = td.text
            x = x.replace(",", ".")
            if cpt == 0:
                data['commune'] = x
                cpt += 1

            elif cpt == 1:
                data['code_INSEE'] = x
                cpt += 1

            elif cpt == 2:
                x = x.replace(" ", "")
                x = re.sub("\.[0-9]*", "", x)
                data['code_postal'] = int(x)
                cpt += 1

            elif cpt == 3:
                x = x.replace(" ", "")
                data['population'] = int(x)
                cpt += 1

            elif cpt == 4:
                x = x.replace(" ", "")
                data['superficie (km²)'] = float(x)
                cpt += 1

            elif cpt == 5:
                x = x.replace(" ", "")
                data['densité (hab./km²)'] = float(x)
                cpt += 1

    return data


def list_info_communes(communes):
    list_communes = []
    if communes == "Paris":
        list_communes.append(info_commune(communes))
    else:
        for td in communes:
            list_communes.append(info_commune(td))
    return list_communes


def create_csv_departement():
    soup = create_soup()
    df = pd.DataFrame.from_dict(list_info_communes(get_tableau_communes(soup)))
    path = "/Users/maelribes/PycharmProjects/PROJ632_Scraping_Villages/csvFiles/" + departement + ".csv"
    df.to_csv(path, index=False, header=True)


def create_csv_france():
    list_dep = get_list_departement()
    list_communes = []
    for dep in tqdm(list_dep, bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:50}{r_bar}'):
        soup = create_soup_from(dep)
        list_communes.extend(list_info_communes(get_tableau_communes(soup)))
    df = pd.DataFrame.from_dict(list_communes)
    df.to_csv("/Users/maelribes/PycharmProjects/PROJ632_Scraping_Villages/csvFiles/Communes_Fr.csv", index=False, header=True)


def affichage_village_from_departement():
    l = list_info_communes(get_tableau_communes(create_soup()))
    for dict in l:
        print(dict)


