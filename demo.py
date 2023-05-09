import pandas as pd

path = "/Users/rasmus/Desktop/Mapper & Filer/Skole/Hovedforløb/H4/Python/Pollen/LuxPollen/data.csv"

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

dato = '1992-07-15'
print(pollen_data_for_date(pollen_data, dato))

## HENT DATA FOR UGE NR
def pollen_data_for_week_number(pollen_data, year, week_number):
    pollen_data['Date'] = pd.to_datetime(pollen_data['Date'])  # Convert Date column to datetime
    week_mask = pollen_data.loc[pollen_data['Date'].dt.year == year]
    week_mask = week_mask.loc[week_mask['Date'].dt.isocalendar().week == week_number]
    return week_mask

year = 1992
week_number = 29
print(f"Pollen fra uge {week_number}")
print(pollen_data_for_week_number(pollen_data, year, week_number))


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


