#-------------------------------------//---------------------------------------
#-----------------------------------------------------------------------------
#                  MATRIZ BINARIA E EXTRAÇÃO DE CARACTERISTICA  
#-----------------------------------------------------------------------------
#-------------------------------------//--------------------------------------


#-------------------------------------
# BIBLIOTECA 
#-------------------------------------

import nibabel as nib
import numpy as np
#from scipy.io import  savemat
from six.moves import range
from radiomics import base, cMatrices, deprecated, featureextractor
import os 
import radiomics
from radiomics import glcm, glrlm, glszm, ngtdm
import nrrd
import sys

#-------------------------------------
# LEITURA .NPY
#-------------------------------------

#regioes = np.load('Lista_final_interseccao.npy')    

#savemat("/Users/Lab/Documents/Murilo/GLCM/" "all_regions_nodes.mat",{"regioes":regioes})    

#-------------------------------------
#LISTA DE PACIENTES (.txt)
#------------------------------------

id_call = int(sys.argv[1])

with open('E:/RFAlzheimers_CIPAC/final_test_2_final.txt','r') as f:
    lines = f.readlines()

path_base = 'E:/RFAlzheimers_CIPAC/brain_mat_matrices/'
path_out = 'C:/Users/kaueu/Desktop/SIPAIM_ValParaiso_Chile/'
#uncomment in case want to generate list of interest regions    
patients = list()
for idx,subject_name in enumerate(lines):
    
    subject_name = subject_name.replace('\n','')
    patients.append(subject_name)
    #print(subject_name)
    patient_region = np.load(path_base+subject_name+'/list_region_label.npy')
    if idx==0:
        regions=patient_region    
        #print('a')
    else:
        regions=np.intersect1d(regions,patient_region)


patients = np.array(patients)
patients = np.split(patients,10)[id_call]
regions = regions[1:]

#-------------------------------------
# CONDIÇÃO (Todas as regiões em todos os pacientes (for pacientes + for regiões))
#-------------------------------------

#pacientes = pacientes[0:10]
    
    
for patient in patients:
    
    n1_sMRI = np.load(path_base+patient+'/orig.npy')
    #paciente[0] = 'N8' 
    #wherefMRI = '/Users/Lab/Documents/Murilo/DataSet_RM/TESTE_REGISTRO/'+ paciente[0] + '/fmri_registered_fo_ECC.nii.gz'
    #n1_fMRI = nib.load (wherefMRI) 
    #n1_fMRI = n1_fMRI.get_fdata()  
    
    nrrd.write(path_out+'patient'+str(id_call)+'.nrrd', n1_sMRI)
    #print('---------------------------------------------------------------------------------------1')
    
    #savemat('/Users/Lab/Documents/Murilo/Extracao_Matriz_Binaria/'+ paciente[0] + "/fMRI.mat", {"volume":n1_fMRI})
    
    #img = nib.load('/Users/Lab/Documents/Murilo/DataSet_RM/TESTE_REGISTRO/'+ paciente[0] + '/aparc.DKTatlas+aseg.nii.gz')
    #img.shape
    #img2 = img.get_data()
    try:
        os.mkdir(path_out+patient)
    except:
        print(patient+': Folder already existent')
    
    for region in regions:
        #data = img2.copy()
        #data = (data==regiao)*1
        region_data = np.load(path_base+patient+'/reg_'+str(region)+'.npy')
        nrrd.write(path_out+'region'+str(id_call)+'.nrrd', region_data*1)
        #print('---------------------------------------------------------------------------------------2')
        print(patient + ' - ' + str(region))

#-------------------------------------
# GLCM
#-------------------------------------   

        #dataDir = os.path.join(os.getcwd(), '/Users/Lab/Documents/Murilo/GLCM/'+ paciente[0])
        
        #print("dataDir, relative path", dataDir)
        #print("dataDir, absolute path", os.path.abspath(dataDir))

#Leitura da Imagem e Mascara

       # img = os.path.join('n1_fMRI')
       # mask = os.path.join('data')

        
        #paramPath = os.path.join(os.getcwd(), '/Users/Lab/Documents/Murilo/GLCM/'+ paciente[0], 'Params.yaml')
        
       # print ('Parameter file, absolute path', os.path.abspath(paramPath))

#Extração de caracteristicas

        extractor = featureextractor.RadiomicsFeatureExtractor()

        
        #print('Extraction parameters:\n\t', extractor.settings)
        #print('Enabled filters:\n\t', extractor.enabledImagetypes)
        #print('Enabled features:\n\t', extractor.enabledFeatures)

#Resultado
        
        result = extractor.execute(path_out+'patient'+str(id_call)+'.nrrd', path_out+'region'+str(id_call)+'.nrrd')
        
        #print ('Result type:', type(result))
        #print('')
        #print('Calculated features')
        
        lista = [] #Criar lista vazia
        
        for key, value in result.items():
           if '_glcm' in key:
               lista.append(value)
              # print("/t", key, ":", value)
           if '_glrlm' in key:
               lista.append(value)
               #print("/t", key, ":", value)
           if '_glszm' in key:
               lista.append(value)
               #print("/t", key, ":", value)
           if '_ngtdm' in key:
               lista.append(value)
               #print("/t", key, ":", value)
               
        np.save(path_out + patient + '/reg_' + str(region), lista)

        #break
    #break
    
                  
  
           # savemat("/Users/Lab/Documents/Murilo/Extracao_Matriz_Binaria/"+paciente[0]+"/regiao_"+str(regiao)+".mat", {"mask":data})

