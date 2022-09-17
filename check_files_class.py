#-------------------------------------//--------------------------------------
#                          GERAR MATRIZ DE REGIÕES
#-------------------------------------//--------------------------------------

import numpy as np
import pandas as pd

path_base = 'C:/Users/kaueu/Desktop/SIPAIM_ValParaiso_Chile/'
path_out = 'C:/Users/kaueu/Desktop/SIPAIM_ValParaiso_Chile/Matrices/Matriz_'

regions = np.load('list_regions.npy')

patients = np.load('patients.npy')
patients = [x.replace('\n','') for x in patients]

df_total = pd.read_csv(path_base+'entire_dataset_freesurfer.csv')
df_patient = pd.DataFrame(patients,columns=['Subject'])

int_df = pd.merge(df_patient, df_total, how='inner', on=['Subject'])[['Age','Subject','Group']]
int_df = int_df.drop_duplicates()




#--------------------------------------------------
# condition (Todos os pacientes em todas as regiao
#--------------------------------------------------


    
            
   # np.save(path_out + str(region), matriz)
    
  #  xxx = np.load(path_out+'2.npy')

# =============================================================================
#                            GERAR MATRIZ DE REGIÕES
# =============================================================================
