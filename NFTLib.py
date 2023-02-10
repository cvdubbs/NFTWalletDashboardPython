from web3 import Web3
import json
import requests
from pandas import json_normalize 
import pandas as pd
import numpy as np

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
    df = pd.DataFrame.from_dict(dicty['ownedNfts'])
    while ('pageKey' in dicty):
        pk_next = dicty['pageKey']
        url = "https://eth-mainnet.g.alchemy.com/nft/v2/DDEUdTIi3FXhHcYRDTff8jVeSiz3dZwC/getNFTs?owner={}&pageKey={}&pageSize=100&withMetadata=true".format(walletaddress, pk_next)
        response = requests.get(url, headers=headers)
        data = response.text
        dicty = json.loads(data)
        df_add = pd.DataFrame.from_dict(dicty['ownedNfts']) 
        frames = [df, df_add]
        df = pd.concat(frames)
    df = df.reset_index()
    df['name'] = np.NaN
    df['token_address'] = np.NaN
    for i in df.index:
        try:
            pain_dict = df['contractMetadata'].loc[i]
            pain2_dict = df['contract'].loc[i]
            df['name'].loc[i] = (pain_dict['name'])
            df['token_address'].loc[i] = (pain2_dict['address'])
        except:
            pain_dict = df['contractMetadata'].loc[i]
            pain2_dict = df['contract'].loc[i]
            sub_dict = pain_dict['openSea']
            df['name'].loc[i] = sub_dict['collectionName']
            df['token_address'].loc[i] = (pain2_dict['address'])
    df = df[['name', 'token_address']]
    df = df.groupby(df.columns.tolist(), as_index=False).size()
    df = df.reset_index()
    df = df.drop(columns='index')
    return df

def get_os_vol(contractAddy):
    url = f"https://api.nftport.xyz/v0/transactions/stats/{contractAddy}?chain=ethereum"
    headers = {
        "accept": "application/json",
        "Authorization": "5de0f827-ce62-4eb7-95d9-6615f20d4b53"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    dicty = json.loads(data)
    df = pd.DataFrame.from_dict(dicty)
    if df.iloc[0,0] == 'NOK':
        return 0
    else:
        fp_df = df.loc[df.index == 'floor_price']
        tv_df = df.loc[df.index == 'total_volume']
        try:
            return tv_df.iloc[0,1]
        except:
            return 0

def GetCombine(walletaddress):
    """
    Combine both NFTs_owned and get_os_floor with one function

    Parameters
    ----------
    walletaddress : str
        Ethereum Mainnet walletaddress


    Returns
    -------
    dataframe
        All NFTs owned and floor prices cleaned up
    """
    nfts_owned_ed = NFTs_owned_alchemy(walletaddress)
    nfts_owned_ed["floor_price"] = np.nan
    nfts_owned_ed["total_volume"] = np.nan
    for index, row in nfts_owned_ed.iterrows():
        nfts_owned_ed.total_volume[index] = get_os_vol(nfts_owned_ed.token_address[index])
        nfts_owned_ed.floor_price[index] = get_os_floor(nfts_owned_ed.token_address[index])
    nfts_owned_ed.loc[ nfts_owned_ed["floor_price"] == "unable to fetch floor price", "floor_price"] = 0
    nfts_owned_ed["total"] = nfts_owned_ed['floor_price'] * nfts_owned_ed['size']
    return nfts_owned_ed
