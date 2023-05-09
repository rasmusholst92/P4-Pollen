import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def main():
    actualization_date = get_actualization_date()
    urls = get_pollen_urls(actualization_date)
    pollen_data = get_pollens(urls)
    weather_data = get_weather_data()
    data = merge_pollen_and_weather(weather_data, pollen_data, actualization_date)
    print(data)


def merge_pollen_and_weather(weather_data, pollen_data, actualization_date):
    # fletter vejrdata og pollendata ud fra deres datoer
    data = pd.merge(weather_data, pollen_data, left_on='Date', right_on='Date', how='outer')
    data = data[(data.index >= '1992-01-01') & (data.index < actualization_date)]
    # indsætter 0 hvor data mangler
    data = data.fillna(0)
    # beregner gennemsnits temp
    data['Mean Temperature'] = (data['High Temperature'] + data['Low Temperature']) / 2
    data['Year'] = data.index
    data['Year'] = data['Year'].dt.year
    data['Day of year'] = data.index
    data['Day of year'] = data['Day of year'].dt.dayofyear    
    data.ne(0).idxmax()
    
    # gemmer til data.csv
    data.to_csv('data.csv', index=True)

    return data


def get_weather_data():
    # henter vejrdata og nanvgivner kolonnerne
    weather_data = pd.read_csv('https://data.public.lu/en/datasets/r/a67bd8c0-b036-4761-b161-bdab272302e5',
                               encoding='latin', index_col=0, parse_dates=True, dayfirst=True)
    weather_data.columns = ['High Temperature', 'Low Temperature', 'Precipitation']
    
    # sætter indexet til dato format
    weather_data.index = pd.to_datetime(weather_data.index, dayfirst=True, format="mixed")
    weather_data.index.name = "Date"

    return weather_data


def get_actualization_date():
    # scraper hjemmeside og finder 'Actualisation'
    response = requests.get("http://www.pollen.lu/index.php?qsPage=data&year=1992&week=0&qsLanguage=Fra")
    soup = BeautifulSoup(response.text, 'html.parser')
    html_tables = soup.find_all('table')
    pollen_table = html_tables[5]
    date_start = pollen_table.text.find('Actualisation: ') + 15
    actualization_date_str = pollen_table.text[date_start:date_start + 10]

    return datetime.strptime(actualization_date_str, '%d.%m.%Y')

def get_pollen_urls(actualization_date):
    weekly_url = []

    # henter URL for hver uge fra 1992 til actualization_date.year
    for year in range(1992, actualization_date.year + 1):
        url_year = 'http://www.pollen.lu/index.php?qsPage=data&year='+str(year)+'&week=0&qsLanguage=Fra'
        response = requests.get(url_year)
        soup = BeautifulSoup(response.text, 'html.parser')
        html_tables = soup.find_all('table')
        link_table = html_tables[5]

        # tilføjer URLer fra link_table til weekly_url listen
        for option in link_table.find_all('option'):
            link = option['value']
            url_year_week = 'http://www.pollen.lu/'+link
            weekly_url.append(url_year_week)

    # fjerner ugyldige URLer
    for _ in range(4):
        weekly_url.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=&qsLanguage=Fra')

    return weekly_url


def get_pollens(weekly_url):
    pollen_dfs = []

    # henter data fra hver URL i weekly_url
    for url_weekly_data in weekly_url:
        response = requests.get(url_weekly_data)
        soup = BeautifulSoup(response.text, 'html.parser')
        html_tables = soup.find_all('table')
        pollen_table = html_tables[5]
        pollen_df = pollen_df_from_table(pollen_table)
        pollen_dfs.append(pollen_df)

        print(f"Got pollen: {datetime.now()}")

    # concatter alle dataframes i pollen_dfs liste
    return pd.concat(pollen_dfs, ignore_index=False)

def pollen_df_from_table(pollen_table):
    dfs = pd.read_html(str(pollen_table))
    df = dfs[0].iloc[1:, :].copy()
    df.columns = dfs[1].values.tolist()[0]
    
    df = df.transpose()
    df.columns = df.iloc[1:2, :].values[0].tolist()
    df = df.drop(['Français', 'Latin', 'Deutsch', 'Lëtzebuergesch'])
    
    # sætter datoformat som index
    df.index.name = 'Date'
    df.index = pd.to_datetime(df.index)
    
    # konvertere værdierne i dataframet til floats
    df = df.astype(float)
    
    return df

main()