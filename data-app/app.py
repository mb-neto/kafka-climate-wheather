import os, sys
import pandas as pd
import numpy as np
import json, time
from utils import _print, _error, _warning
from database import upsert_firerisks_data


#INPE: https://queimadas.dgi.inpe.br/queimadas/dados-abertos/#

COUNTRY='33'
STATE='13'
INPE_API_LINK=f'https://queimadas.dgi.inpe.br/api/focos/?pais_id={COUNTRY}&estado_id={STATE}' # pais_id=33(br) e estado_id=13(amazonas)

_print("> Start data-app!")
_print('> Contacting INPE API...')
_print(f'  Country: ({COUNTRY})')
_print(f'  State: ({STATE})')
_print(f'  API Link: ({INPE_API_LINK})')

while (True):
    _print("> Sending request...")
    try:
        df_queimadas = pd.read_json(INPE_API_LINK)
        df_queimadas["geometry"] = df_queimadas["geometry"].map(lambda item: json.dumps(item))
        df_queimadas["properties"] = df_queimadas["properties"].map(lambda item: json.dumps(item))

        _print("> Data collected: ")
        print(df_queimadas.head())  # Dataframe first row
        print(df_queimadas.count()) # Data info
        print(df_queimadas.columns) # Dataframe columns

        upsert_firerisks_data(df_queimadas)
    except Exception as e:
        _error("> Request failed!")
        _error(e)
        _warning("> Trying again in 5min...")
        time.sleep(300)
        _warning("Restart!".center(40, "-"))
    else:
        _print("> Time interval! (24h)")
        time.sleep(86400000) #86400 (24h)
        _print("End of time interval!".center(40, "#") + "\n")