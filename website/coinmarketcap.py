from datetime import datetime 
import requests
import json
import pandas as pd 


def get_coin_id(symbol='BTC'):
    coin_ids = pd.read_csv('./coinmarketcap/coin_ids.csv')
    id = coin_ids.loc[coin_ids['coin']==symbol, 'id'].values[0]
    return str(id)


def date_to_timestamp(date):
    datetime_fmt = datetime.strptime(date, '%Y-%m-%d')
    timestamp = datetime_fmt.timestamp()
    return int(timestamp)


def api_get_hist_data(coin_id, currency_id, date_start, date_end):

    time_start_tmstp = date_to_timestamp(date_start)
    time_end_tmstp = date_to_timestamp(date_end)

    api_call_url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={coin_id}&convertId={currency_id}&timeStart={time_start_tmstp}&timeEnd={time_end_tmstp}'

    api_res = requests.get(api_call_url).json()

    df = pd.json_normalize(pd.DataFrame(api_res['data']['quotes'])['quote'])

    return df


def api_get_ticker(coin_id, currency_id):

    api_call_url = f'https://web-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={coin_id}&convert_id={currency_id}'

    api_res = requests.get(api_call_url).json()

    price = api_res['data'][coin_id]['quote'][currency_id]['price']

    return price


if __name__ == '__main__':

    currency_id = '2790' # unique coinmarketcap ID for EUR
    coin = 'DOGE'
    start_date = '2010-04-28'
    end_date = '2021-05-31'
    coin_id = get_coin_id(coin)

    df = api_get_hist_data(coin_id, currency_id, start_date, end_date)
    print(df)

    df.to_csv(f'./coinmarketcap/historic_data_{coin}_to_EUR_{start_date}_to_{end_date}.csv', index=False)

    #df = api_get_ticker(coin_id, currency_id)
    #print(df)


