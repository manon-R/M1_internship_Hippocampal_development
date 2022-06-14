import os
import ants
import numpy as np
import pandas as pd
import csv
import pingouin as pg
from statistics import mean

vol_T1 = pd.read_csv("/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_seg-hsf_volumes.csv")
vol_T2 = pd.read_csv("/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_seg-hsf_volumes_T2.csv")
R1_T1 = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_R1.csv') 
R1_T2 = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_R1_T2.csv') 

patients_sub = {"sub-07P":"Right", "sub-13P":"Left","sub-18P": "Left","sub-19P":"Right","sub-20P":"Right","sub-32P":"Left", "sub-34P":"Right", "sub-31C" : ""}
SUBFIELDS = ["DG", "CA1", "CA2", "CA3", "Subiculum"]

def total_vol_per_side(db, side):
    return sum([db[f"{field}-{side}"] for field in SUBFIELDS])


def total_hipp_volume(db):
    return (total_vol_per_side(db, "Left") + total_vol_per_side(db, "Right")) /2


def R1_data_from_csv(subfield, side, db): #No side for T2 R1
    R1_data = []
    for d in db[f"{subfield}-{side}"]:
        d = d.replace("[", "")
        d = d.replace("]", "")
        R1_data.append(mean(list(map(float, d.split(", "))))) #Subfield R1 rates mean / subject
    return R1_data 

def total_R1(db):
    return (sum([np.array(R1_data_from_csv(field, "Left", db)) for field in SUBFIELDS])/len(SUBFIELDS) + sum([np.array(R1_data_from_csv(field, "Right", db)) for field in SUBFIELDS])/len(SUBFIELDS)) / 2


#T1 data : 
controls_vol_T1 = vol_T1[~vol_T1.Subject.isin(patients_sub)]
patients_vol_T1 = vol_T1[vol_T1.Subject.isin(patients_sub)]
controls_R1_T1 = R1_T1[~R1_T1.Subject.isin(patients_sub)]
patients_R1_T1 = R1_T1[R1_T1.Subject.isin(patients_sub)]

#T2 data : 
controls_vol_T2 = vol_T2[~vol_T2.Subject.isin(patients_sub)]
patients_vol_T2 = vol_T2[vol_T2.Subject.isin(patients_sub)]
controls_R1_T2 = R1_T2[~R1_T2.Subject.isin(patients_sub)]
patients_R1_T2 = R1_T2[~R1_T2.Subject.isin(patients_sub)]

datas = {"T1 Control group Volumes":controls_vol_T1,
        "T2 Control group Volumes" : controls_vol_T2,
        "T1 Patient group Volumes" : patients_vol_T1, 
        "T2 Patient group Volumes" : patients_vol_T2,
        "T1 Control group R1":controls_R1_T1,
        "T2 Control group R1" : controls_R1_T2,
        "T1 Patient group R1" : patients_R1_T1, 
        "T2 Patient group R1" : patients_R1_T2} 

# Note : Only one male patient ! 
datas_Gender = {"T1 Control group Female Volumes":controls_vol_T1[controls_vol_T1.Gender == 'F' ],
        "T1 Control group Male Volumes":controls_vol_T1[controls_vol_T1.Gender == 'M' ],  
        "T2 Control group Female Volumes":controls_vol_T2[controls_vol_T2.Gender == 'F' ],
        "T2 Control group Male Volumes":controls_vol_T2[controls_vol_T2.Gender == 'M' ],
        "T1 Patient group Female Volumes" : patients_vol_T1[patients_vol_T1.Gender == 'F' ], 
        "T2 Patient group Female Volumes" : patients_vol_T2[patients_vol_T2.Gender == 'F' ],
        "T1 Control group Female R1":controls_R1_T1[controls_R1_T1.Gender == 'F' ],
        "T1 Control group Male R1":controls_R1_T1[controls_R1_T1.Gender == 'M' ],
        "T2 Control group Female R1" : controls_R1_T2[controls_R1_T2.Gender == 'F' ],
        "T2 Control group Male R1":controls_R1_T2[controls_R1_T2.Gender == 'M' ],
        "T1 Patient group Female R1" : patients_R1_T1[patients_R1_T1.Gender == 'F' ], 
        "T2 Patient group Female R1" : patients_R1_T2[patients_R1_T2.Gender == 'F' ]} 

def normality_test(datas : dict):
    print("Normality Distribution Test")
    for k, v in datas.items():
        print(f"{k} : " )
        print(pg.normality(v))

#normality_test(datas_Gender)




#Correlation coefficient

# Total R1 and Age correlation
print(pg.corr(controls_R1_T1["Age"], total_R1(controls_R1_T1)))

# Total hipp volume and Age correlation Male / Female
print(pg.corr(controls_vol_T1[controls_vol_T1.Gender == 'M']["Age"], total_hipp_volume(controls_vol_T1[controls_vol_T1.Gender == 'M'])))
print(pg.corr(controls_vol_T1[controls_vol_T1.Gender == 'F']["Age"], total_hipp_volume(controls_vol_T1[controls_vol_T1.Gender == 'F'])))




#T-test

#Gender effect : Statistical differences Male / Female
print("\nGender effect on total hippocampal volumes estimation : \n")
print(pg.ttest(total_hipp_volume(controls_vol_T1[controls_vol_T1.Gender == 'M']), total_hipp_volume(controls_vol_T1[controls_vol_T1.Gender == 'F']))) 



#T1-T2 ROIs volumes  comparison
controls_T1_right = total_vol_per_side(controls_vol_T1[~controls_vol_T1.Subject.isin(["sub-32P", "sub-34P"])], "Right")
controls_T2_right = total_vol_per_side(controls_vol_T2,"Right")

controls_T1_left = total_vol_per_side(controls_vol_T1[~controls_vol_T1.Subject.isin(["sub-32P", "sub-34P"])], "Left")
controls_T2_left = total_vol_per_side(controls_vol_T2,"Left")

print("\nT1-T2 ROIs Volumes T-Test (Right and Left): \n")
print(pg.ttest(controls_T1_right, controls_T2_right, paired=True)) 
print(pg.ttest(controls_T1_left, controls_T2_left, paired=True)) 

#p-value controls right = 1e⁻⁶
#p-value controls left = 4.58e⁻⁷