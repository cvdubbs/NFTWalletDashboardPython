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

NFTs_owned('0xE74dFE8d4dbd080f6c0cb34A11CFbACBFE315439')
