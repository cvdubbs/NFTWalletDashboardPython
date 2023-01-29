import Quants.NFTLib
from Quants.NFTLib import GetCombine, NFTs_owned_alchemy, get_os_floor, NFTs_owned
from web3 import Web3
import json
import requests
from pandas import json_normalize 
from moralis import evm_api
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.secret_key = 'df16dd57a6f502ac06ce8f71'

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        walletaddress = request.form['WalletAddy']
        df = GetCombine(walletaddress)
        df = df.drop(columns=(['token_address','urlname']))
        df = df[df.floor_price >= .000001]
        df = df.rename(columns={"size": "Quantity", "total": "Total", "floor_price":"Floor Price"})
        df = df.sort_values(by='Total', ascending=False)
        return render_template('index.html', column_names=df.columns.values, row_data=list(df.values.tolist()),zip=zip)
    return render_template('index.html')

# Pranksy
# 0xD387A6E4e84a6C86bd90C158C6028A58CC8Ac459
#Flurdao
# 0x5e9c948A7197D4c83D71dC869b4f0Eb968cafC7a
# print(GetCombine('0x5e9c948A7197D4c83D71dC869b4f0Eb968cafC7a')) 