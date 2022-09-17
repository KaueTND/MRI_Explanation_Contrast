#-------------------------------------//--------------------------------------
#                          GERAR MATRIZ DE REGIÕES
#-------------------------------------//--------------------------------------

import numpy as np

path_base = 'C:/Users/kaueu/Desktop/SIPAIM_ValParaiso_Chile/'
path_out = 'C:/Users/kaueu/Desktop/SIPAIM_ValParaiso_Chile/Matrices/Matriz_'

regions = np.load('list_regions.npy')

lines = np.load('patients.npy')
#--------------------------------------------------
# CONDIÇÃO (Todos os pacientes em todas as regiões 
#--------------------------------------------------


for region in regions:
    
    for it, patient in list(enumerate(lines)):
        patient = patient.replace('\n','')
        a = np.load(path_base+ patient+ '/reg_' + str(region) + '.npy')
        
        if it == 0:
            matriz = a
           
        else:
            matriz = np.vstack((matriz,a))
                     
    
            
    np.save(path_out + str(region), matriz)
    
    xxx = np.load(path_out+'2.npy')

# =============================================================================
#                            GERAR MATRIZ DE REGIÕES
# =============================================================================
