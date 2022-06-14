import os
import ants
import numpy as np
import pandas as pd
import csv

DIRECTORY_NAME_R1 = '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/derivatives/T1map-mathrip'
DIRECTORY_NAME_T1 = '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/derivatives/T1seg-hsf'
DIRECTORY_NAME_T2 = '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/derivatives/2022-06_T2_T1_registration_yl' # !! Bilateral segmentation !!
EXCLUDED_SUB_T1 = ["00C", "01C", "02C", "code"]
EXCLUDED_SUB_T2 = ["00C", "01C", "02C", "code", "31C", "32P", "34P"] # 32P and 34P excluded as they have no T2

def retrieve_R1_T1():
	relax_data = []
	count = 0
	subject_age = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/rawdata/participants.tsv', delimiter = '\t', usecols=['age'], skiprows= lambda x:x in [ 1, 2, 3, 32]).values
	subject_gender = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/rawdata/participants.tsv', delimiter = '\t', usecols=['sex'], skiprows= lambda x:x in [ 1, 2, 3, 32]).values  

	sub_folder = sorted(os.listdir(DIRECTORY_NAME_T1), key=lambda x:int(x[4:6]))

	for folder in sub_folder:
		
		if any([True if sub in folder else False for sub in EXCLUDED_SUB_T1]):
			pass

		else:
			
			folder_pathT1 = os.path.join(DIRECTORY_NAME_T1, folder + "/anat")

			#Hippocampal ROI's R1 rates (for n=29)
			relax_data.append([folder, subject_age[count][0].replace(",", "."), subject_gender[count][0]])
			file_pathR1 = os.path.join(DIRECTORY_NAME_R1, f"{folder}/anat/{folder}_R1map.nii.gz")
			R1_data = ants.image_read(file_pathR1) 
			R1_map = R1_data.numpy()
			count += 1
			
			for file in os.listdir(folder_pathT1):
				file_path = os.path.join(folder_pathT1, file)
				if "left" in file_path:
					
					left_hipp = ants.image_read(file_path)
					left_hipp_mat = left_hipp.numpy()
					relax_data[-1]+= [list(R1_map[left_hipp_mat == i]) for i in range(1,6)] 
					
			
				else:
					right_hipp = ants.image_read(file_path)
					right_hipp_mat = right_hipp.numpy()				
					
					relax_data[-1]+= [list(R1_map[right_hipp_mat == i]) for i in range(1,6)] 

	np.savetxt('hippocampus_R1.csv', relax_data, fmt= "%s", delimiter=',', header='Subject,Age,Gender,DG-Left,CA1-Left,CA2-Left,CA3-Left,Subiculum-Left,DG-Right,CA1-Right,CA2-Right,CA3-Right,Subiculum-Right', comments='') 

	""" with open("hippocampus_R1.csv", "w+") as file:
		new_array = csv.writer(file)
		new_array.writerow(["Subject", "Age", "Gender", "DG-Left", "CA1-Left", "CA2-Left", "CA3-Left", "Subiculum-Left", "DG-Right", "CA1-Right", "CA2-Right", "CA3-Right", "Subiculum-Right"])
		new_array.writerows(relax_data) """



#R1 from bilateral T2 ROIs in T1 space  !! 

def retrieve_R1_T2():
	relax_data = []
	count = 0

	#Retrieve age and gender
	subject_age = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/rawdata/participants.tsv', delimiter = '\t', usecols=['age'], skiprows= lambda x:x in [ 1, 2, 3, 32]).values
	subject_gender = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/rawdata/participants.tsv', delimiter = '\t', usecols=['sex'], skiprows= lambda x:x in [ 1, 2, 3, 32]).values 


	sub_folder = sorted(os.listdir(DIRECTORY_NAME_T2), key=lambda x:int(x[4:6]))

	for folder in sub_folder:
		if any([True if sub in folder else False for sub in EXCLUDED_SUB_T2]):
			pass

		else:
			file_path_T2_in_T1 = os.path.join(DIRECTORY_NAME_T2, f"{folder}/anat/{folder}_acq-HR_rec-hiplay7recombine_T2w_bilat_hippocampus_in_T1w_space.nii.gz")
			relax_data.append([folder, subject_age[count][0].replace(",", "."), subject_gender[count][0]])
			file_pathR1 = os.path.join(DIRECTORY_NAME_R1, f"{folder}/anat/{folder}_R1map.nii.gz")
			R1_data = ants.image_read(file_pathR1) 
			R1_map = R1_data.numpy()
			count += 1

			seg_hipp = ants.image_read(file_path_T2_in_T1)
			seg_hipp_mat = seg_hipp.numpy()
			relax_data[-1]+= [list(R1_map[seg_hipp_mat == i]) for i in range(1,6)]


	with open("hippocampus_R1_T2.csv", "w+") as file:
		new_array = csv.writer(file)
		new_array.writerow(["Subject", "Age", "Gender", "DG", "CA1", "CA2", "CA3", "Subiculum"])
		new_array.writerows(relax_data)
