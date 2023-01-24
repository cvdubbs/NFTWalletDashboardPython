# Setup
from web3 import Web3
import json
import requests
from pandas import json_normalize 
import pandas as pd

def get_os_floor(contractid):
    """
    Get NFT Floor by collection contract

    Parameters
    ----------
    contractid : str
        Ethereum Mainnet contract id


    Returns
    -------
    float
        OpenSea Floor Value
    """
    alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/DDEUdTIi3FXhHcYRDTff8jVeSiz3dZwC"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    url = "https://eth-mainnet.g.alchemy.com/nft/v2/DDEUdTIi3FXhHcYRDTff8jVeSiz3dZwC/getFloorPrice?contractAddress={}".format(contractid)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.text
    dicty = json.loads(data)
    df = pd.DataFrame.from_dict(dicty)
    return df.iloc[0,0]

# print(get_os_floor("0xe785E82358879F061BC3dcAC6f0444462D4b5330"))