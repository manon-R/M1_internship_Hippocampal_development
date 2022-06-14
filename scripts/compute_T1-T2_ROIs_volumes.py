import os
import ants
import numpy as np
import pandas as pd
import csv

'''First script to test volumes' computation (hsf segmentation) L/R 
Correspondance checked compare to itk-snap results'''


DIRECTORY_NAME_T1 = '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/derivatives/T1seg-hsf' # de 03C à 34P
DIRECTORY_NAME_T2 = '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/derivatives/hsf_hiplayrec' # de 03C à 30C 

EXCLUDED_SUB = ["00C", "01C", "02C", "code", "31C", "32P", "34P"] #["00C", "01C", "02C", "code"] for T1 seg

volumes_data = []
relax_data = []
count = 0
subject_age = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/rawdata/participants.tsv', delimiter = '\t', usecols=['age'], skiprows= lambda x:x in [ 1, 2, 3, 32]).values
subject_gender = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/rawdata/participants.tsv', delimiter = '\t', usecols=['sex'], skiprows= lambda x:x in [ 1, 2, 3, 32]).values  

#sub_folder = sorted(os.listdir(DIRECTORY_NAME_T1), key=lambda x:int(x[4:6]))
sub_folder = sorted(os.listdir(DIRECTORY_NAME_T2), key=lambda x:int(x[4:6]))

for folder in sub_folder:
	
	if any([True if sub in folder else False for sub in EXCLUDED_SUB]):
		pass

	else:
		#Hippocampal ROI's volumes (in mm³)
		
		volumes_data.append([folder, subject_age[count][0].replace(",", "."), subject_gender[count][0]])
		#folder_pathT1 = os.path.join(DIRECTORY_NAME_T1, folder + "/anat")
		folder_pathT2 = os.path.join(DIRECTORY_NAME_T2, folder + "/anat")
		count += 1
		
		for file in os.listdir(folder_pathT2):
			file_path = os.path.join(folder_pathT2, file)
			if "left" in file_path:
				
				left_hipp = ants.image_read(file_path)
				left_hipp_mat = left_hipp.numpy()
				volumes_data[-1] += [round(np.count_nonzero(left_hipp_mat == i)*(0.125*1.2*0.125), 2) for i in range(1,6)]
				#volumes_data[-1] += [round(np.count_nonzero(left_hipp_mat == i)*(0.75**3), 2) for i in range(1,6)] T1 isotropic voxel
				
			else:
				right_hipp = ants.image_read(file_path)
				right_hipp_mat = right_hipp.numpy()					
				volumes_data[-1] += [round(np.count_nonzero(right_hipp_mat == i)*(0.125*0.125*1.2), 2) for i in range(1,6)]
				#volumes_data[-1] += [round(np.count_nonzero(right_hipp_mat == i)*(0.75**3), 2) for i in range(1,6)] T1 isotropic voxel
				
			
	
data = np.array(volumes_data, dtype='unicode')


np.savetxt('hippocampus_seg-hsf_volumes_T2_test.csv', data, fmt="%s", delimiter=',', header='Subject,Age,Gender,DG-Left,CA1-Left,CA2-Left,CA3-Left,Subiculum-Left,DG-Right,CA1-Right,CA2-Right,CA3-Right,Subiculum-Right', comments='') 


# to merge CA2-CA3 directly when saving data in csv
""" for i in range(1,6):
					if i == 4:
						volumes_data[-1][-1] += round(np.count_nonzero(left_hipp_mat == i)*(0.75**3), 2)
						volumes_data[-1][-1] = round(volumes_data[-1][-1], 2)
					else:	
						volumes_data[-1].append(round(np.count_nonzero(left_hipp_mat == i)*(0.75**3), 2))

for i in range(1,6):
					if i == 4:
						volumes_data[-1][-1] += round(np.count_nonzero(right_hipp_mat == i)*(0.75**3), 2)
						volumes_data[-1][-1] = round(volumes_data[-1][-1], 2)
					else:	
						volumes_data[-1].append(round(np.count_nonzero(right_hipp_mat == i)*(0.75**3), 2))

data = np.array(volumes_data, dtype='unicode')

np.savetxt('hippocampus_seg-hsf_vol_unified.csv', data, fmt="%s", delimiter=',', header='Subject,Age,Gender,DG-Left,CA1-Left,CA2-CA3-Left,Subiculum-Left,DG-Right,CA1-Right,CA2-CA3-Right,Subiculum-Right', comments='') 
 """