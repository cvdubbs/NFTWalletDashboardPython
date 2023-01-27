# from NFTLib import *
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Pranksy
# 0xD387A6E4e84a6C86bd90C158C6028A58CC8Ac459
#Flurdao
# 0x5e9c948A7197D4c83D71dC869b4f0Eb968cafC7a
# print(GetCombine('0x5e9c948A7197D4c83D71dC869b4f0Eb968cafC7a')) 