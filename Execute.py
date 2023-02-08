import NFTLib
from NFTLib import GetCombine, NFTs_owned_alchemy, get_os_floor
from web3 import Web3
import json
import requests
from pandas import json_normalize 
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, url_for, flash, redirect
import yfinance as yf

app = Flask(__name__)
app.secret_key = 'df16dd57a6f502ac06ce8f71'

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        walletaddress = request.form['WalletAddy']
        df = GetCombine(walletaddress)
        df = df.dropna()
        df = df.drop(columns=(['token_address']))
        df = df[df.floor_price >= .000001]
        df = df[df.total_volume >= .1]
        df = df.rename(columns={"size": "Quantity", "total": "Total", "floor_price":"Floor Price", "total_volume":"Total Volume"})
        df = df.sort_values(by='Total', ascending=False)
        # df['Floor Price'] = df['Floor Price'].round(4)
        # df['Total'] = df['Total'].round(4)
        df['Total Volume'] = df['Total Volume'].astype(int)
        TotalEth = df['Total'].sum()
        TotalEth = round(TotalEth,4)
        ethp = yf.Ticker("ETH-USD")
        todays_data = ethp.history(period='1d')
        ethusd = todays_data['Close'][0]
        ethusd = round(ethusd,2)
        totalusd = (ethusd*TotalEth)
        totalusd = round(totalusd,0)
        totalval = f"The Total Usd Value of this wallet is: ${totalusd}"
        ethprice = f"The ETH/USD Price is ${ethusd}"
        totaletht = f"The Total Eth Value of this wallet is: {TotalEth}"
        return render_template('index.html', column_names=df.columns.values, row_data=list(df.values.tolist()),zip=zip, totalval=totalval, ethprice=ethprice, totaletht=totaletht)
    return render_template('index.html')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()