import pandas as pd


def sort_csv(csv,colonne,ordre):
    if ordre == 'croissant':
        o = True
    elif ordre == 'décroissant' or 'décroissant':
        o = False
    else:
        return print('Ordre invalide')

    if colonne == 'code postal':
        c = 'code_postal'
    elif colonne == 'population' or 'commune':
        c = colonne
    elif colonne == 'superficie':
        c = 'superficie (km²)'
    elif colonne == 'densité' or 'densite':
        c = 'densité (hab./km²)'
    else:
        return print('Colonne invalide')

    path = '/Users/maelribes/PycharmProjects/PROJ632_Scraping_Villages/csvFiles/' + csv + '.csv'
    df = pd.read_csv(path, index_col='commune')
    df = df.sort_values(by=[c], ascending=o)
    df.to_csv(path)