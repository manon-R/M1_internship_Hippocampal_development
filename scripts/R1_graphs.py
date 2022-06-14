import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean

sns.set_theme()

data = pd.read_csv('/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_R1.csv') #hippocampus_R1_T2.csv
PATIENTS = ["sub-07P", "sub-13P","sub-18P","sub-19P","sub-20P","sub-32P","sub-34P"]
controls = data[~data.Subject.isin(PATIENTS)] #Keep only control subjects
patients = data[data.Subject.isin(PATIENTS)]
SUBFIELDS = ["DG", "CA1", "CA2", "CA3", "Subiculum"]
LABELS = ["Controls", "Patients"]


#Retrieve R1 mean from csv file
def R1_data_from_csv(subfield, side, db): #No side for T2 R1
    R1_data = []
    for d in db[f"{subfield}-{side}"]:
        d = d.replace("[", "")
        d = d.replace("]", "")
        R1_data.append(mean(list(map(float, d.split(", "))))) #Subfield R1 rates mean / subject
    return R1_data 

def R1_CA2_CA3_unified(side, db): # by doing mean(mean(CA2), mean(CA3))
    CA2_R1 = np.array(R1_data_from_csv("CA2", side, db))
    CA3_R1 = np.array(R1_data_from_csv("CA3", side, db))
    return (CA2_R1+CA3_R1)/2


def total_R1_per_side(db, side):
    return sum([np.array(R1_data_from_csv(field, side, db)) for field in SUBFIELDS])/len(SUBFIELDS)

def total_R1(db):
    return (sum([np.array(R1_data_from_csv(field, "Left", db)) for field in SUBFIELDS])/len(SUBFIELDS) + sum([np.array(R1_data_from_csv(field, "Right", db)) for field in SUBFIELDS])/len(SUBFIELDS)) / 2



def plot_total_hipp_R1_RL_controls():
    f, (ax1, ax2) = plt.subplots(1,2, sharey=True)
    
    sns.regplot(data=controls[controls.Gender == 'F'], x="Age", y=total_R1_per_side(controls[controls.Gender == 'F'], "Left"), ax=ax1, color = "#d25c7e")#, lowess=True
    sns.regplot(data=controls[controls.Gender == 'F'], x="Age", y=total_R1_per_side( controls[controls.Gender == 'F'], "Right"), ax=ax2, label="Controls F", color= "#d25c7e")
    sns.regplot(data=controls[controls.Gender == 'M'], x="Age", y=total_R1_per_side(controls[controls.Gender == 'M'],  "Left"), ax=ax1, color = "blue")#, lowess=True
    sns.regplot(data=controls[controls.Gender == 'M'], x="Age", y=total_R1_per_side(controls[controls.Gender == 'M'], "Right"), ax=ax2, label="Controls M", color= "blue")
    
   
    ax1.set_xlabel("Age (year)")
    ax2.set_xlabel("Age (year)")
    ax1.set_ylabel("R1 rate")
    ax1.set_title("Left")
    ax2.set_title("Right")
    ax2.legend()
    f.suptitle(f"Total hippocampal R1 rates (Right / Left)", fontsize=16)
    
    plt.show()



def plot_hipp_R1_subfield_controls_patients(subfield): # +/- subfield as parameter for other subfield
    f, (ax1, ax2) = plt.subplots(1,2, sharey=True, sharex=True)
    sns.regplot(data=controls[controls.Gender == 'F' ], x="Age", y=(np.array(R1_data_from_csv(subfield,"Left", controls[controls.Gender == 'F' ])) + np.array(R1_data_from_csv("Subiculum","Right",controls[controls.Gender == 'F' ])))/2, ax= ax1 ,color = "#d25c7e", label="Controls",)#, lowess=True  ,color = "#ae0c20"
    sns.regplot(data=controls[controls.Gender == 'M' ], x="Age", y=(np.array(R1_data_from_csv(subfield,"Left",controls[controls.Gender == 'M' ])) + np.array(R1_data_from_csv("Subiculum","Right",controls[controls.Gender == 'M' ])))/2, ax= ax2, label="Controls")
    #sns.regplot(data=controls, x="Age", y=total_R1(controls),  label="Controls") 

    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion == "Left"]["Age"], R1_data_from_csv(subfield, "Left", patients[patients.Gender == 'F'][patients.Lesion == "Left"]), color="#ae0c20",label = "Ipsilesional", marker="s")
    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion != "Left"]["Age"], R1_data_from_csv(subfield, "Left", patients[patients.Gender == 'F'][patients.Lesion != "Left"]), color="#ae0c20", label="Contralesional") 
    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion == "Right"]["Age"],R1_data_from_csv(subfield, "Right",patients[patients.Gender == 'F'][patients.Lesion == "Right"]) , color="#ae0c20", marker="s") 
    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion != "Right"]["Age"], R1_data_from_csv(subfield, "Right",patients[patients.Gender == 'F'][patients.Lesion != "Right"]) , color="#ae0c20") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion == "Left"]["Age"], R1_data_from_csv(subfield, "Left", patients[patients.Gender == 'M'][patients.Lesion == "Left"]), color="blue", label = "Ipsilesional", marker="s") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion != "Left"]["Age"], R1_data_from_csv(subfield, "Left", patients[patients.Gender == 'M'][patients.Lesion != "Left"]), color="blue", label="Contralesional") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion == "Right"]["Age"], R1_data_from_csv(subfield, "Right", patients[patients.Gender == 'M'][patients.Lesion == "Right"]), color="blue" , marker="s") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion != "Right"]["Age"], R1_data_from_csv(subfield, "Right",patients[patients.Gender == 'M'][patients.Lesion != "Right"]), color="blue" ) 
 


    #Annotate each subject point : To be adpated for each subfield
    for age in  patients[patients.Gender == 'F']["Age"]:
        ax1.text(patients[patients.Gender == 'F'][patients.Age == age].Age+ 0.02, ((R1_data_from_csv(subfield, "Right", patients[patients.Gender == 'F'][patients.Age == age])[0] + R1_CA2_CA3_unified( "Left", patients[patients.Gender == 'F'][patients.Age == age])[0])/2) -0.045,patients[patients.Gender == 'F'][patients.Age == age]["Subject"].values[0], verticalalignment = "center", horizontalalignment="center", rotation="vertical", size="small", color = 'black', weight= "semibold" )
    for age in  patients[patients.Gender == 'M']["Age"]:
        
        ax2.text(patients[patients.Gender == 'M'][patients.Age == age].Age+ 0.02, R1_data_from_csv(subfield, "Right", patients[patients.Gender == 'M'][patients.Age == age])[0] - 0.03,patients[patients.Gender == 'M'][patients.Age == age]["Subject"].values[0], verticalalignment = "center", horizontalalignment="center", rotation="vertical",size="small" , color = 'black', weight= "semibold" )
       

    ax1.set_xlabel("Age (year)")
    ax2.set_xlabel("Age (year)")
    
    ax1.set_title("Female", loc="center" ,fontsize=12, fontweight="bold")
    ax2.set_title("Male", loc="center",  fontsize=12, fontweight="bold")

    ax1.set_ylabel("R1 rate")
    ax1.set_ylim(0.5, 0.87)
    ax1.legend()
    ax2.legend()
    f.suptitle(f"{subfield} R1 rate", fontsize=20)
    plt.show()

    #plt.savefig(f"./Plots/R1_subfields/R1_C-P/{subfield}-R1rates_C-P.png")
        
""" for subfield in SUBFIELDS:
    plot_hipp_R1_subfield_controls_patients(subfield) """



#Plot R1 histogram per subfield - side of control group
def plot_R1_hist_per_subfield(subfield, side):
    R1_data = [] #Keep all R1 values from specific subfield column
    for d in controls[f"{subfield}-{side}"]:
        
        d = d.replace("[", "")
        d = d.replace("]", "")
        R1_data = R1_data + list(map(float, d.split(", ")))


    print(f"Max : {max(R1_data)}, Min : {min(R1_data)}") #

    #plt.hist(R1_data, bins = 20, range=(min(R1_data), max(R1_data)), log=True)

    sns.histplot(data = R1_data, binwidth=0.2, log_scale=(False, True))
    plt.title(f"{subfield} R1 rates ({side}, Controls, n=23) ", fontsize=16)
    plt.xlabel("R1 rate")
    plt.xlim(0, 5.2) #5.2 max of all subfields 
    plt.show() 


