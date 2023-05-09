import pandas as pd

path = "/Users/rasmus/Desktop/Mapper & Filer/Skole/Hovedforløb/H4/Python/Pollen/LuxPollen/data.csv"

### DEL 1 ###

## HENT ALT DATA
def read_pollen_date(path):
    pollen_data = pd.read_csv(path)
    return pollen_data


pollen_data = read_pollen_date(path)
print(pollen_data.head())

## HENT DATA FOR EN BESTEMT DAG
def pollen_data_for_date(pollen_data, date):
    date_mask = pollen_data[pollen_data["Date"] == date]
    return date_mask
    pollen_data_for_date = pollen_data_for_date(pollen_data, date)


print(pollen_data_for_date(pollen_data, "1992-07-15"))

### DEL 2 ###

## FØRSTE DAG PÅ ÅRET MED POLLEN
def get_first_day_with_pollen(pollen_data, year):
    data_by_year = pollen_data[pollen_data['Year'] == year]
    pollen_columns = ['Ambrosia', 'Artemisia', 'Asteraceae', 'Alnus', 'Betula', 'Ericaceae',
                      'Carpinus', 'Castanea', 'Quercus', 'Chenopodium', 'Cupressaceae', 'Acer',
                      'Fraxinus', 'Gramineae', 'Fagus', 'Juncaceae', 'Aesculus', 'Larix', 'Corylus',
                      'Juglans', 'Umbellifereae', 'Ulmus', 'Urtica', 'Rumex', 'Populus', 'Pinaceae',
                      'Plantago', 'Platanus', 'Salix', 'Cyperaceae', 'Filipendula', 'Sambucus', 'Tilia']

    first_pollen_day = data_by_year[data_by_year[pollen_columns].gt(0).any(axis = 1)].iloc[0]

    return first_pollen_day

year = 1992
result = get_first_day_with_pollen(pollen_data, year)
print(f"Første dag med pollen i {year} var {result['Date']}.")


