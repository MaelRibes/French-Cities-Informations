import pandas as pd


def sort_csv(csv, colonne, ordre):
    if ordre == 'croissant':
        o = True
    elif ordre == 'décroissant' or ordre == 'decroissant':
        o = False
    else:
        raise Exception('Ordre invalide')

    if colonne == 'code postal':
        c = 'code_postal'
    elif colonne == 'population' or colonne == 'commune':
        c = colonne
    elif colonne == 'superficie':
        c = 'superficie (km²)'
    elif colonne == 'densité' or colonne == 'densite':
        c = 'densité (hab./km²)'
    else:
        raise Exception('Colonne invalide')

    path = '/Users/maelribes/PycharmProjects/PROJ632_Scraping_Villages/csvFiles/' + csv + '.csv'
    df = pd.read_csv(path, index_col='commune')
    df = df.sort_values(by=[c], ascending=o)
    df.to_csv(path)


# def search_info()