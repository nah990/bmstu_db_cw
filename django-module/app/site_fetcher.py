# scraper.py
import requests
from .data_formatter import date_conversion, float_conversion, number_of_days_in_month
import lxml
from bs4 import BeautifulSoup
import yfinance as yf
import random


def gov_capital(ticket):
    url = 'https://gov.capital/stock/' + ticket + '-stock/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    raw_data = soup.find_all('td', {'class': ['text-align-right', 'text-align-left']})
    forecast_date_data = []
    i = 0
    for data in raw_data:
        i = i + 1
        if i == 1:
            forecast_date_data.append(date_conversion(data.text))
            continue
        forecast_date_data.append(float_conversion(data.text))
        if i == 4:
            i = 0
    return forecast_date_data


def leo_prophet(ticket):
    months = [('Jan', '01'), ('Feb', '02'), ('Mar', '03'),
              ('Apr', '04'), ('May', '05'), ('Jun', '06'),
              ('Jul', '07'), ('Aug', '08'), ('Sep', '09'),
              ('Oct', '10'), ('Nov', '11'), ('Dec', '12')]
    year = 2021
    full_data = []
    while year < 2026:
        url = 'https://leoprophet.com/stock_forecasts/forecast_' + ticket + '/for' + str(year) + '/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        raw_data = soup.find_all('tbody', class_='tbodyStyle')
        data_text = raw_data[0].text
        data_text = data_text.replace(' %   ', '\n')
        data_text = data_text.replace(' %', '')
        data_text = data_text.strip()
        data_text = data_text.split('\n')

        for data in data_text:
            for k, v in months:
                data = data.replace(k, v)
            month = int(data[0]) * 10 + int(data[1])
            for j in range(number_of_days_in_month(year, month)):
                i = j + 1
                month_str = str(month)
                i_str = str(i)
                if month < 10:
                    month_str = '0' + str(month)
                if i < 10:
                    i_str = '0' + str(i)
                date = str(year) + '-' + month_str + '-' + i_str
                min_num = float_conversion(data.split(' ')[2])
                max_num = float_conversion(data.split(' ')[3])
                rand_num = random.randrange(int(min_num), int(max_num))
                full_data.append(date)
                full_data.append(rand_num)
                full_data.append(min_num)
                full_data.append(max_num)
        year = year + 1
    return full_data


def get_name_by_ticket(ticket):
    yfobj = yf.Ticker(ticket)
    return yfobj.info['longName']

data = gov_capital("spce")
print(data)