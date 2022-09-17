# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 22:09:43 2022

@author: kaueu
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 09:58:45 2022

@author: kaueu
"""
from statsmodels.stats.multitest import fdrcorrection as fdrcorrection
import researchpy as rp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

NCvMCI = pd.read_csv('HNvMCI_descriptor.csv')
MCIvAD = pd.read_csv('MCIvAD_descriptor.csv')
NCvAD  = pd.read_csv('HNvAD_descriptor.csv')

NCvMCI = NCvMCI[['pos','name','sum']]
MCIvAD = MCIvAD[['pos','name','sum']]
NCvAD = NCvAD[['pos','name','sum']]

df_final = pd.merge(NCvMCI,MCIvAD,how='left',on='name')
df_final = pd.merge(df_final,NCvAD,how='left',on='name')
df_final['total'] = df_final['pos_x']+df_final['pos_y']+df_final['pos']  
df_final = df_final.sort_values(by='total')
df_final = df_final[['name','pos_x','pos_y','pos','sum_x','sum_y','sum','total']]