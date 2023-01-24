from web3 import Web3
import json
import requests
from pandas import json_normalize 
from moralis import evm_api
import pandas as pd
import numpy as np


def NFTs_owned(walletaddress):
    """
    Get NFTs owned by walletaddress

    Parameters
    ----------
    walletaddress : str
        Ethereum Mainnet Address


    Returns
    -------
    dataframe
        Name, ContractID, Quantity
    """
    api_key = "xeulBfSFsvTH7mW2tJLrBY6J4YdtrKJr7of9ydrUhqnmcGzajyMdZa8Np3HGF09K"
    params = {
        "address": walletaddress, 
        "chain": "eth", 
        "format": "decimal", 
        "limit": 100, 
        "token_addresses": [], 
        "cursor": "", 
        "normalizeMetadata": True, 
    }
    result = evm_api.nft.get_wallet_nfts(
        api_key=api_key,
        params=params,
    )
    result_df = pd.DataFrame.from_dict(result['result'])
    result_df = result_df[['name','token_address']]
    result_df = result_df.groupby(result_df.columns.tolist(), as_index=False).size()
    result_df['urlname'] = result_df['name'].str.lower()
    result_df['urlname'] = result_df['urlname'].str.replace(' ','-')
    return result_df


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

def NFTs_owned_alchemy(walletaddress):
    alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/DDEUdTIi3FXhHcYRDTff8jVeSiz3dZwC"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    url = "https://eth-mainnet.g.alchemy.com/nft/v2/DDEUdTIi3FXhHcYRDTff8jVeSiz3dZwC/getNFTs?owner={}&pageSize=100&withMetadata=true".format(walletaddress)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.text
    dicty = json.loads(data)
    df = pd.DataFrame.from_dict(dicty['ownedNFTs'])
    return df