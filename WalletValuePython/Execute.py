from NFTLib import *
import pandas as pd
import numpy as np

nfts_owned_ed = NFTs_owned('0x5e9c948A7197D4c83D71dC869b4f0Eb968cafC7a')
nfts_owned_ed["floor_price"] = np.nan
for index, row in nfts_owned_ed.iterrows():
    nfts_owned_ed.floor_price[index] = get_os_floor(nfts_owned_ed.token_address[index])
nfts_owned_ed.loc[ nfts_owned_ed["floor_price"] == "unable to fetch floor price", "floor_price"] = 0
nfts_owned_ed["total"] = nfts_owned_ed['floor_price'] * nfts_owned_ed['size']
print(nfts_owned_ed)