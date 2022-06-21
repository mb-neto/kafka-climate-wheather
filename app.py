#INPE: https://queimadas.dgi.inpe.br/queimadas/dados-abertos/#
#INMET: 

import os, sys
import pandas as pd
import numpy as np

API_LINK='/home/manoelbenedito/Documentos/faculdade/tcc/dados/focos24h_estados_RN.csv'

df = pd.read_csv(API_LINK, parse_dates=['data_hora_gmt'])

print(df.head()) # Visualize dataframe head

print(df.describe()) # Describes dataframe info