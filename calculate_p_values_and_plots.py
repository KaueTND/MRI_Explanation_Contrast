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


##### PLEASE UPDATE YOUR BASE_DIR HERE
base_dir = 'your/directory/'
base_dir = 'C:/Users/kaueu/Desktop/All/SIPAIM_ValParaiso_Chile/'
chosen_stage_1 = 'HN'
chosen_stage_2 = 'MCI'

def generate_values(regs,path_base,path_out,chosen_stage_1,chosen_stage_2):
    lista_descritores = np.load('lista_descritores.npy')
    super_vec_feature = np.zeros((len(regs),61))
    mean_values_master = np.zeros((len(regs),61))
    random_indices = np.random.choice(100, size=70, replace=False)
    for idx,reg in enumerate(regs):
        matrix_aux = np.ones(61)
        mean_values = np.ones(61)
        print(reg)
        #for id_row,desc in enumerate(group_descriptors):
        matrix = np.load(path_base+str(reg)+'.npy')
        #print(matrix.shape)
        for feature in range(matrix.shape[1]):
            
            matrix_CN = matrix[types[chosen_stage_1][0]:types[chosen_stage_1][1],feature]
            matrix_AD = matrix[types[chosen_stage_2][0]:types[chosen_stage_2][1],feature]
            
            
            matrix_CN = matrix_CN[random_indices]
            matrix_AD = matrix_AD[random_indices]
            group_cn  = pd.DataFrame(matrix_CN)
            group_ad  = pd.DataFrame(matrix_AD)
            
            #print(group_cn[0])
            val = rp.ttest(group1=group_cn[0], group1_name= chosen_stage_1, group2=group_ad[0], group2_name= chosen_stage_2)
            #if(val[1].loc[3]['results']<0.05):
            matrix_aux[feature] = val[1].loc[3]['results']
            mean_values[feature] = val[1].loc[0]['results']
                #print(feature)
                #print(val[1].loc[3]['results'])
        super_vec_feature[idx]=(matrix_aux)
        mean_values_master[idx]=(mean_values)
        lista_descritores = np.arange(61)
    df = pd.DataFrame(super_vec_feature,columns=lista_descritores)
    df2 = pd.DataFrame(mean_values_master,columns=lista_descritores)
    #df['regioes_nome'] = 
    df['regioes_id'] = regs
    df.to_csv(path_out+'_p_value.csv')
    df2['regioes_id'] = regs
    df2.to_csv(path_out+'_mean_values.csv')
    
    return [super_vec_feature,mean_values_master]


path_base = base_dir+'Matrices/Matriz_'

regs = np.load(base_dir+'list_regions.npy')

patients = np.load(base_dir+'patients.npy')
patients = [x.replace('\n','') for x in patients]
    
list_regions_organized = pd.read_csv(base_dir+'list_regions_organized.txt',sep = ',')







types = {'HN':[0,100],
         'eMCI':[100,200],
         'MCI':[200,300],
         'lMCI':[300,400],
         'AD':[400,500]}

case = chosen_stage_1+'v'+chosen_stage_2

path_out = base_dir+case

case = chosen_stage_1+ ' vs '+chosen_stage_2

[super_vec_feature,mean_values] = generate_values(regs,path_base,path_out,chosen_stage_1,chosen_stage_2)


# ##########################
df = pd.read_csv(path_out+'_p_value.csv')
df = df.set_index('Unnamed: 0')

df_mean = pd.read_csv(path_out+'_mean_values.csv')
df_mean = df_mean.set_index('Unnamed: 0')

df = pd.merge(list_regions_organized,df,how='left',on='regioes_id')
df_mean = pd.merge(list_regions_organized,df_mean,how='left',on='regioes_id')
#sns.heatmap(df_mean)



super_vec_feature = np.array(df)[:,2:].astype('float')
mean_values = np.array(df_mean)[:,2:].astype('float')
regs=df['regioes_id']
#nome=df['regioes_nome']
#lista_descritores = df.columns[0:-1]
test = super_vec_feature<0.05
lista_descritores = np.load(base_dir+'lista_descritores.npy')

color_image_left = np.array([1,2,1,2,3,3,1,2,1,2,
                    1,2,1,2,1,2,1,2,3,3,
                    3,3,3,1,2,1,2,1,2,1,
                    2,1,2,1,2,1,2,1,2,1,
                    2,1,2,1,2,1,2,1,2,1,
                    2,1,2,1,2,1,2,1,2,1,
                    2,1,2,1,2,1,2,1,2,1,
                    2,1,2,1,2,1,2,1,2,1,
                    2,1,2,1,2])

color_image_left = np.array([color_image_left]*61)[:,:].T




#plt.figure()
#sns.heatmap(mean_values>0)
################### PLOT THE DESCRIPTORS OR REGIONS
ax=0

summ = np.sum(test,axis=ax)
if ax==1:
    summ = np.vstack((summ,regs)).T
else:
    summ = np.vstack((summ,lista_descritores)).T

df2 = pd.DataFrame(summ)
df2[0] = pd.to_numeric(df2[0])

#import seaborn as sns
#import matplotlib.pyplot as plt

df2 = df2.sort_values(by=0)

#print(np.arange(len(df2[1])))
#plt.figure(figsize=(14,5))
#plt.title('P-values')
#plt.plot(np.arange(len(df2[1])),df2[0])
#plt.xticks(np.arange(len(df2[1])),df2[1],rotation=90)

####################################### PLOT THE P_VALUE MATRIX

# plt.figure(figsize=(15,15))
# plt.title('p-values')

# #super_vec_feature = np.nan_to_num(super_vec_feature)

# #print(super_vec_feature)

# ax = sns.heatmap(super_vec_feature.astype('float32'),cmap='bwr')

# font = {'family' : 'normal',
#         'weight' : 'regular',
#         'size'   : 22}

# plt.rc('font', **font)

# #nome = nome.to_numpy()
# lista_descritores = lista_descritores.to_numpy()
# plt.xticks(np.arange(len(lista_descritores)),lista_descritores,rotation=45,ha='right')
# plt.yticks(np.arange(len(regs)),regs,rotation=45)

# for n, label in enumerate(ax.xaxis.get_ticklabels()):
#     if n % 5 != 0:
#         label.set_visible(False)

# for n, label in enumerate(ax.yaxis.get_ticklabels()):
#     if n % 5 != 0:
#         label.set_visible(False)

# plt.savefig(path_out+'pvalues_part.png',bbox_inches='tight')


########################################################## PLOT THE UNCORRECTED VALUES


#plt.figure(figsize=(12,15))
#plt.title('uncorrected p<0.05')
#ax = sns.heatmap(test,cbar=None,cmap='gray')


#font = {'family' : 'normal',
#        'weight' : 'regular',
#        'size'   : 22}

#plt.rc('font', **font)

#plt.xticks(np.arange(len(lista_descritores)),lista_descritores,rotation=45,ha='right')
#plt.yticks(np.arange(len(regs)),regs,rotation=45)

#for n, label in enumerate(ax.xaxis.get_ticklabels()):
#    if n % 5 != 0:
#        label.set_visible(False)

#for n, label in enumerate(ax.yaxis.get_ticklabels()):
#    if n % 5 != 0:
#        label.set_visible(False)

#plt.savefig(path_out+'p-values_uncorr_part.png',bbox_inches='tight')


############################################################ PLOT THE CORRECTED VALUES


#plt.figure(figsize=(12,15))

fdrcorrected = list()
fdr_values = list()
for x in super_vec_feature:
    fdrcorrected.append(fdrcorrection(x,alpha=0.05)[0])
    fdr_values.append(fdrcorrection(x,alpha=0.05)[1])
fdrcorrected = np.array(fdrcorrected)
fdr_values = np.array(fdr_values)
fdrcorrected_df = pd.DataFrame(data=fdrcorrected,columns=lista_descritores.ravel(),index=regs.ravel())

#show_x = np.sum(fdrcorrected,axis=0)
#show_y = np.sum(fdrcorrected,axis=1)

#font = {'family' : 'normal',
#        'weight' : 'regular',
#        'size'   : 22}

#plt.rc('font', **font)

#plt.title('corrected p<0.05')

#plt.imshow(fdrcorrected,cmap='gray')
#ax = sns.heatmap(fdrcorrected_df,cbar=None,cmap='gray')

#every_nth=20
#plt.xticks(np.arange(len(lista_descritores)),lista_descritores,rotation=45,ha='right')
#plt.yticks(np.arange(len(regs)),regs,rotation=45)

#for n, label in enumerate(ax.xaxis.get_ticklabels()):
#    if show_x[n] == 0:
#        label.set_visible(False)

#for n, label in enumerate(ax.yaxis.get_ticklabels()):
#    if show_y[n] == 0:
#        label.set_visible(False)

#plt.savefig(path_out+'p-values_last_part.png',bbox_inches='tight')




#### ALL THE PLOTS 

#####################################################################################PLOT DIFFERENCE 

fig = plt.figure(figsize=(12,15))
plt.title(case+' - Difference '+chosen_stage_1+' (Red) - '+chosen_stage_2+' (Blue)')
mean_values_n = mean_values*1./np.max(mean_values, axis=0)
ax = sns.heatmap(mean_values_n.astype('float32'),cmap='bwr',cbar=None)
font = {'family' : 'normal',
        'weight' : 'regular',
        'size'   : 22}

plt.rc('font', **font)
plt.xlabel('Texture Features')
plt.ylabel('Brain Regions')
#
#set the labels
xticks = [ 11, 32, 48, 61]
xticks_minor = [ 23, 40, 56]
yticks = [1.8,7.1,8.8,11.1,12.8,14.6,16.9,19.5,30.1,47.1,58.1,72.1,83.5]#[3, 17.9, 34, 42,74]
yticks_minor = [6,8,10,12,14,16,18,23,47,55,69,83]#yticks_minor = [18, 33, 38, 70]
ylbls=['Ven','T','C','P','U','H','A','CC','Frontal','Occipital','Temporal','Parietal','In']#ylbls = [ 'Left dGM', 'Right dGM ', 'CC','Left cortical area','Right cortical area']
xlbls = [ 'GLCM', 'GLRLM', 'GLSZM','NGTDM']
#ax = fig.add_axes( [.05, .1, .9, .85 ] )
#set ticks
ax.set_xticks( xticks )
ax.set_xticklabels( xlbls )
ax.set_xticks( xticks_minor, minor=True )
ax.set_yticks( yticks )
ax.set_yticklabels( ylbls ,rotation=90)
ax.set_yticks( yticks_minor, minor=True )

#set the grid 
#ax.set_xticklabels( xlbls, minor=True )
ax.set_xlim( 0, 61 )
plt.grid(visible=True,color='k',which='minor')
ax.tick_params( axis='x', which='minor', direction='out', length=30 )
ax.tick_params( axis='x', which='major', bottom='off', top='off' )
ax.tick_params( axis='y', which='minor', direction='out', length=30 )
ax.tick_params( axis='y', which='major', bottom='off', top='off' )

plt.savefig(path_out+'_difference.pdf',bbox_inches='tight')


###################################################################################################PVALUES

fig = plt.figure(figsize=(15,15))
plt.title(case+' - p-values')
ax = sns.heatmap(super_vec_feature.astype('float32'),cmap='coolwarm')

font = {'family' : 'normal',
        'weight' : 'regular',
        'size'   : 22}
plt.rc('font', **font)

plt.xlabel('Texture Features')
plt.ylabel('Brain Regions')
#
#set the labels
xticks = [ 11, 32, 48, 61]
xticks_minor = [ 23, 40, 56]
yticks = [1.8,7.1,8.8,11.1,12.8,14.6,16.9,19.5,30.1,47.1,58.1,72.1,83.5]#[3, 17.9, 34, 42,74]
yticks_minor = [6,8,10,12,14,16,18,23,47,55,69,83]#yticks_minor = [18, 33, 38, 70]
ylbls=['Ven','T','C','P','U','H','A','CC','Frontal','Occipital','Temporal','Parietal','In']#ylbls = [ 'Left dGM', 'Right dGM ', 'CC','Left cortical area','Right cortical area']
xlbls = [ 'GLCM', 'GLRLM', 'GLSZM','NGTDM']
#ax = fig.add_axes( [.05, .1, .9, .85 ] )
#set ticks
ax.set_xticks( xticks )
ax.set_xticklabels( xlbls )
ax.set_xticks( xticks_minor, minor=True )
ax.set_yticks( yticks )
ax.set_yticklabels( ylbls ,rotation=90)
ax.set_yticks( yticks_minor, minor=True )

#set the grid 
#ax.set_xticklabels( xlbls, minor=True )
ax.set_xlim( 0, 61 )
plt.grid(visible=True,color='k',which='minor')

ax.tick_params( axis='x', which='minor', direction='out', length=30 )
ax.tick_params( axis='x', which='major', bottom='off', top='off' )

ax.tick_params( axis='y', which='minor', direction='out', length=30 )
ax.tick_params( axis='y', which='major', bottom='off', top='off' )

plt.savefig(path_out+'_pvalues_part.pdf',bbox_inches='tight')

##################################################################################PLOT THRESHOLDED MATRIX

fig = plt.figure(figsize=(12,15))
plt.title(case+' - uncorrected p<0.05')


ax = sns.heatmap(test.astype('float32'),cbar=None,cmap='gray')

font = {'family' : 'normal',
        'weight' : 'regular',
        'size'   : 22}

plt.rc('font', **font)

plt.xlabel('Texture Features')
plt.ylabel('Brain Regions')
#
#set the labels
xticks = [ 11, 32, 48, 61]
xticks_minor = [ 23, 40, 56]
yticks = [1.8,7.1,8.8,11.1,12.8,14.6,16.9,19.5,30.1,47.1,58.1,72.1,83.5]#[3, 17.9, 34, 42,74]
yticks_minor = [6,8,10,12,14,16,18,23,47,55,69,83]#yticks_minor = [18, 33, 38, 70]
ylbls=['Ven','T','C','P','U','H','A','CC','Frontal','Occipital','Temporal','Parietal','In']#ylbls = [ 'Left dGM', 'Right dGM ', 'CC','Left cortical area','Right cortical area']
xlbls = [ 'GLCM', 'GLRLM', 'GLSZM','NGTDM']
#ax = fig.add_axes( [.05, .1, .9, .85 ] )
#set ticks
ax.set_xticks( xticks )
ax.set_xticklabels( xlbls )
ax.set_xticks( xticks_minor, minor=True )
ax.set_yticks( yticks )
ax.set_yticklabels( ylbls ,rotation=90)
ax.set_yticks( yticks_minor, minor=True )

#set the grid 
#ax.set_xticklabels( xlbls, minor=True )
ax.set_xlim( 0, 61 )
plt.grid(visible=True,color='y',which='minor')

ax.tick_params( axis='x', which='minor', direction='out', length=30 )
ax.tick_params( axis='x', which='major', bottom='off', top='off' )

ax.tick_params( axis='y', which='minor', direction='out', length=30 )
ax.tick_params( axis='y', which='major', bottom='off', top='off' )

plt.savefig(path_out+'_pvalues_uncorrected.pdf',bbox_inches='tight')
#################################################################################PLOT MATRIX CORRECTEDVALUES

fig = plt.figure(figsize=(12,15))
plt.title(case+' - corrected p-values')

cmap = ['#000000','#ffff00','#0099ff','#ffffff']
ax = sns.heatmap(fdr_values.astype('float32')*color_image_left,cbar=None,cmap='coolwarm')

font = {'family' : 'normal',
        'weight' : 'regular',
        'size'   : 22}

plt.rc('font', **font)

plt.xlabel('Texture Features')
plt.ylabel('Brain Regions')
#
#set the labels
xticks = [ 11, 32, 48, 61]
xticks_minor = [ 23, 40, 56]
yticks = [1.8,7.1,8.8,11.1,12.8,14.6,16.9,19.5,30.1,47.1,58.1,72.1,83.5]#[3, 17.9, 34, 42,74]
yticks_minor = [6,8,10,12,14,16,18,23,47,55,69,83]#yticks_minor = [18, 33, 38, 70]
ylbls=['Ven','T','C','P','U','H','A','CC','Frontal','Occipital','Temporal','Parietal','In']#ylbls = [ 'Left dGM', 'Right dGM ', 'CC','Left cortical area','Right cortical area']
xlbls = [ 'GLCM', 'GLRLM', 'GLSZM','NGTDM']
#ax = fig.add_axes( [.05, .1, .9, .85 ] )
#set ticks
ax.set_xticks( xticks )
ax.set_xticklabels( xlbls,rotation=0 )
ax.set_xticks( xticks_minor, minor=True )
ax.set_yticks( yticks )
ax.set_yticklabels( ylbls ,rotation=90)
ax.set_yticks( yticks_minor, minor=True )

#set the grid 
#ax.set_xticklabels( xlbls, minor=True )
ax.set_xlim( 0, 61 )
plt.grid(visible=True,color='k',which='minor')

ax.tick_params( axis='x', which='minor', direction='out', length=30 )
ax.tick_params( axis='x', which='major', bottom='off', top='off' )

ax.tick_params( axis='y', which='minor', direction='out', length=30 )
ax.tick_params( axis='y', which='major', bottom='off', top='off' )

plt.savefig(path_out+'_pvalues_corrected_val.pdf',bbox_inches='tight')
#################################################################################PLOT THRESHOLDED MATRIX CORRECTED

fig = plt.figure(figsize=(12,15))
plt.title(case+' - corrected p<0.05')

cmap = ['#000000','#ffff00','#0099ff','#ffffff']
ax = sns.heatmap(fdrcorrected_df.astype('float32')*color_image_left,cbar=None,cmap=cmap)

font = {'family' : 'normal',
        'weight' : 'regular',
        'size'   : 22}

plt.rc('font', **font)

plt.xlabel('Texture Features')
plt.ylabel('Brain Regions')
#
#set the labels
xticks = [ 11, 32, 48, 61]
xticks_minor = [ 23, 40, 56]
yticks = [1.8,7.1,8.8,11.1,12.8,14.6,16.9,19.5,30.1,47.1,58.1,72.1,83.5]#[3, 17.9, 34, 42,74]
yticks_minor = [6,8,10,12,14,16,18,23,47,55,69,83]#yticks_minor = [18, 33, 38, 70]
ylbls=['Ven','T','C','P','U','H','A','CC','Frontal','Occipital','Temporal','Parietal','In']#ylbls = [ 'Left dGM', 'Right dGM ', 'CC','Left cortical area','Right cortical area']
xlbls = [ 'GLCM', 'GLRLM', 'GLSZM','NGTDM']
#ax = fig.add_axes( [.05, .1, .9, .85 ] )
#set ticks
ax.set_xticks( xticks )
ax.set_xticklabels( xlbls,rotation=0 )
ax.set_xticks( xticks_minor, minor=True )
ax.set_yticks( yticks )
ax.set_yticklabels( ylbls ,rotation=90)
ax.set_yticks( yticks_minor, minor=True )

#set the grid 
#ax.set_xticklabels( xlbls, minor=True )
ax.set_xlim( 0, 61 )
plt.grid(visible=True,color='k',which='minor')

ax.tick_params( axis='x', which='minor', direction='out', length=30 )
ax.tick_params( axis='x', which='major', bottom='off', top='off' )

ax.tick_params( axis='y', which='minor', direction='out', length=30 )
ax.tick_params( axis='y', which='major', bottom='off', top='off' )

plt.savefig(path_out+'_pvalues_corrected.pdf',bbox_inches='tight')
######################################################################################## BAR PLOT
plt.figure(figsize=(12,2))
fdr_best_descriptors = np.sum(fdrcorrected,axis=0)
descriptors = np.hstack((['GLCM']*24, ['GLRLM']*16, ['GLSZM']*16,['NGTDM']*5))

fdr_best_descriptors = np.vstack((fdr_best_descriptors,descriptors,lista_descritores))
fdr_best_descriptors_df = pd.DataFrame(fdr_best_descriptors.T,columns=['sum','id','name'])
fdr_best_descriptors_df['sum'] = ((pd.to_numeric(fdr_best_descriptors_df['sum'])/85)*100)
fdr_best_descriptors_df = fdr_best_descriptors_df.sort_values(by='sum',ascending=False)
fdr_best_descriptors_df['pos'] = np.arange(len(fdr_best_descriptors_df))
plt.grid(visible=True,color='#999999',zorder=-1)
glcm  = fdr_best_descriptors_df[fdr_best_descriptors_df['id']=='GLCM']
glrlm = fdr_best_descriptors_df[fdr_best_descriptors_df['id']=='GLRLM']
glszm = fdr_best_descriptors_df[fdr_best_descriptors_df['id']=='GLSZM']
ngtdm = fdr_best_descriptors_df[fdr_best_descriptors_df['id']=='NGTDM']
plt.bar( x = glcm['pos'], height = glcm['sum'], label ='GLCM',color='#ff3300') #'y', label='Training loss')
plt.bar( x = glrlm['pos'], height = glrlm['sum'], label ='GLRLM',color='#0066ff')
plt.bar( x = glszm['pos'], height = glszm['sum'], label ='GLSZM',color='#ffcc00')
plt.bar( x = ngtdm['pos'], height = ngtdm['sum'], label ='NGTDM',color='black')    
plt.ylabel('occurrences (%)')
plt.xlabel('descriptors')
plt.ylim(0,75)
plt.yticks([0,15,30,45,60,75])
ax.set_yticklabels( [0,15,30,45,60,75] ,rotation=90)
plt.title(case)
#plt.yticks(np.arange(0, np.max(fdr_best_descriptors_df['sum']), int(np.max(fdr_best_descriptors_df['sum'])/4)))

fdr_best_descriptors_df.to_csv(path_out+'_descriptor.csv')
plt.savefig(path_out+'_descriptor_pval_corrected.pdf',bbox_inches='tight')



#########################################################################################DIFF

# fig = plt.figure(figsize=(12,15))

# #show_x = np.sum(fdrcorrected,axis=0)
# #show_y = np.sum(fdrcorrected,axis=1)

# #show_x = show_x * np.arange(len(show_x))
# #show_x = show_x[show_x >0]
# #show_y = (show_y>0) * np.arange(len(show_y))
# #show_y = show_y[show_y >0]

# font = {'family' : 'normal',
#         'weight' : 'regular',
#         'size'   : 22}

# plt.rc('font', **font)

# plt.title('Difference TS Higher (Blue) v NC Higher (Red)')
# #(-1 = TS) (+1 = NC)   -1(TS Higher) -  1(NC Higher)
# thresh = ((mean_values.astype('float32')>0)*2)-1

# #plt.imshow(fdrcorrected,cmap='gray')
# ax = sns.heatmap(fdrcorrected*thresh,cmap='bwr',vmin=-1,vmax=1,cbar=None)

# plt.xlabel('Texture Features')
# plt.ylabel('Brain Regions')
# #
# #set the labels
# xticks = [ 11, 32, 48, 61]
# xticks_minor = [ 23, 40, 56]
# yticks = [3, 17.9, 34, 42,74]
# yticks_minor = [18, 33, 38, 70]
# ylbls = [ 'Left dGM', 'Right dGM ', 'CC','Left cortical area','Right cortical area']
# xlbls = [ 'GLCM', 'GLRLM', 'GLSZM','NGTDM']
# #ax = fig.add_axes( [.05, .1, .9, .85 ] )
# #set ticks
# ax.set_xticks( xticks )
# ax.set_xticklabels( xlbls )
# ax.set_xticks( xticks_minor, minor=True )
# ax.set_yticks( yticks )
# ax.set_yticklabels( ylbls ,rotation=90)
# ax.set_yticks( yticks_minor, minor=True )



# #set the grid 
# #ax.set_xticklabels( xlbls, minor=True )
# ax.set_xlim( 0, 61 )
# plt.grid(visible=True,color='#ffffff',which='minor')

# ax.tick_params( axis='x', which='minor', direction='out', length=30 )
# ax.tick_params( axis='x', which='major', bottom='off', top='off' )

# ax.tick_params( axis='y', which='minor', direction='out', length=30 )
# ax.tick_params( axis='y', which='major', bottom='off', top='off' )



# plt.savefig(case+'_difference.pdf',bbox_inches='tight')