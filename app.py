#INPE: https://queimadas.dgi.inpe.br/queimadas/dados-abertos/#
#INMET: 

import os, sys
import pandas as pd
import numpy as np

INPE_API_LINK='https://queimadas.dgi.inpe.br/api/focos/?pais_id=33&estado_id=13' # pais_id=33(br) e estado_id=13(amazonas)

df_queimadas = pd.read_json(INPE_API_LINK)

print(df_queimadas) # Visualize dataframe preview

print(df_queimadas.count()) # Data info