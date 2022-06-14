from cProfile import label
from curses import color_pair
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


sns.set_theme()


# For T2 : data = pd.read_csv('hippocampus_seg-hsf_volumes_T2.csv') #hippocampus_seg-hsf_vol_unified or hippocampus_seg-hsf_volumes or hippocampus_seg-hsf_volumes_T2.csv
data = pd.read_csv("/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_seg-hsf_volumes.csv")
patients_sub = {"sub-07P":"Right", "sub-13P":"Left","sub-18P": "Left","sub-19P":"Right","sub-20P":"Right","sub-32P":"Left", "sub-34P":"Right", "sub-31C" : ""}



#T1 data : 
controls = data[~data.Subject.isin(patients_sub)]
patients = data[data.Subject.isin(patients_sub)]

SUBFIELDS = ["DG", "CA1", "CA2", "CA3", "Subiculum"]


def total_vol_per_side(db, side):
    return sum([db[f"{field}-{side}"] for field in SUBFIELDS]) #for total volume

def vol_per_subfield(db, side, field):
    return db[f"{field}-{side}"]

def total_hipp_volume(db):
    return total_vol_per_side(db, "Left") + total_vol_per_side(db, "Right")



#Plot total volumes of control group = One figure
def plot_total_hipp_volumes_control():
    f, ax = plt.subplots(1,1, sharey=True)
    sns.regplot(data=controls[controls.Gender == 'F' ], x="Age", y=total_hipp_volume(controls[controls.Gender == 'F' ]), color = "#ae0c20", label="Controls F")#, lowess=True 
    sns.regplot(data=controls[controls.Gender == 'M' ], x="Age", y=total_hipp_volume(controls[controls.Gender == 'M' ]),  label="Controls M")
    
    #Whole control group:
    #sns.regplot(data=controls, x="Age", y=total_hipp_vol(controls),  label="Controls")  
    
    ax.set_xlabel("Age (year)")
    ax.set_ylabel("Volume (mm3)")
    ax.legend()
    f.suptitle(f"Total Hippocampal Volumes", fontsize=16)
    plt.show()


#Plot total volumes of control group Left / Right
def plot_hipp_volumes_RL_control():
    f, (ax1, ax2) = plt.subplots(1,2, sharey=True)
    
    sns.regplot(data=controls[controls.Gender == 'F' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'F' ], "Left"), ax=ax1,color = "#ae0c20")#, lowess=True  
    sns.regplot(data=controls[controls.Gender == 'M' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'M' ], "Left"), ax=ax1)
    sns.regplot(data=controls[controls.Gender == 'F' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'F' ], "Right"), ax=ax2,color = "#ae0c20", label="Controls F")
    sns.regplot(data=controls[controls.Gender == 'M' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'M' ], "Right"), ax=ax2, label="Controls M")
       
    ax1.set_xlabel("Age (year)")
    ax2.set_xlabel("Age (year)")
    ax1.set_ylabel("Volume (mm3)")
    ax1.set_title("Left")
    ax2.set_title("Right")
    ax2.legend()
    f.suptitle(f"Total Hippocampal Volumes (Left / Right)", fontsize=16)
    plt.show()




#Mean for controls + Ipsi / Contra for patients
def plot_volumes_per_subfield(subfield):
    f, (ax1, ax2) = plt.subplots(1,2, sharey=True, sharex = True)
    # for total : y=compute_total_hipp_volume(controls[controls.Gender == 'F'])/2,
    sns.regplot(data=controls[controls.Gender == 'F'], x=np.append(controls[controls.Gender == 'F']["Age"],controls[controls.Gender == 'F']["Age"]), y=np.append(vol_per_subfield(controls[controls.Gender == 'F'], "Left", subfield), vol_per_subfield(controls[controls.Gender == 'F'], "Right", subfield) ), ax=ax1,label="Controls", color = "#d25c7e")
    sns.regplot(data=controls[controls.Gender == 'M'], x=np.append(controls[controls.Gender == 'M']["Age"],controls[controls.Gender == 'M']["Age"]), y=np.append(vol_per_subfield(controls[controls.Gender == 'M'], "Left", subfield), vol_per_subfield(controls[controls.Gender == 'M'], "Right", subfield) ), ax=ax2, label="Controls", scatter_kws= {"color": "#a5c4f8"})


    axes = [ax1, ax2]

    count=0

    for ax in axes:
        
        ax.set_ylabel("Volume (mm3)")
        ax.set_xlabel("Age (year)")    
        #ax.set_ylim(min([min(controls['CA2-CA3-Left']), min(controls['CA2-CA3-Right'])]),max([max(controls['CA2-CA3-Left']), max(controls['CA2-CA3-Right'])])) #+/- 50
        ax.set_title("Female", loc="center") if count == 0 else ax.set_title("Male", loc="center")
        count += 1 

    #A automatiser en for loop sur ["Right", "Left"]
    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion == "Left"]["Age"], vol_per_subfield(patients[patients.Gender == 'F'][patients.Lesion == "Left"], "Left", subfield), color="#ae0c20",label = "Ipsilesional", marker="s")
    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion != "Left"]["Age"], vol_per_subfield(patients[patients.Gender == 'F'][patients.Lesion != "Left"], "Left", subfield), color="#ae0c20", label="Contralesional") 
    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion == "Right"]["Age"],vol_per_subfield(patients[patients.Gender == 'F'][patients.Lesion == "Right"] , "Right", subfield), color="#ae0c20", marker="s") 
    ax1.scatter(patients[patients.Gender == 'F'][patients.Lesion != "Right"]["Age"],vol_per_subfield(patients[patients.Gender == 'F'][patients.Lesion != "Right"], "Right", subfield), color="#ae0c20") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion == "Left"]["Age"], vol_per_subfield(patients[patients.Gender == 'M'][patients.Lesion == "Left"], "Left", subfield), color="blue", label = "Ipsilesional", marker="s") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion != "Left"]["Age"], vol_per_subfield(patients[patients.Gender == 'M'][patients.Lesion != "Left"], "Left", subfield), color="blue", label="Contralesional") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion == "Right"]["Age"],vol_per_subfield(patients[patients.Gender == 'M'][patients.Lesion == "Right"], "Right", subfield), color="blue" , marker="s") 
    ax2.scatter(patients[patients.Gender == 'M'][patients.Lesion != "Right"]["Age"],vol_per_subfield(patients[patients.Gender == 'M'][patients.Lesion != "Right"], "Right", subfield), color="blue" ) 


    #Annotate each subject point : To be adpated for each subfield
    for age in  patients[patients.Gender == 'F']["Age"]:
        ax1.text(patients[patients.Gender == 'F'][patients.Age == age].Age + 0.05, vol_per_subfield(patients[patients.Gender == 'F'][patients.Age == age], "Right", subfield) - 50,patients[patients.Gender == 'F'][patients.Age == age]["Subject"].values[0], verticalalignment = "center", horizontalalignment="center", rotation="vertical", size="small", color = 'black', weight= "semibold" )
    for age in  patients[patients.Gender == 'M']["Age"]:
        ax2.text(patients[patients.Gender == 'M'][patients.Age == age].Age, vol_per_subfield(patients[patients.Gender == 'M'][patients.Age == age], "Right", subfield)+50,patients[patients.Gender == 'M'][patients.Age == age]["Subject"].values[0], verticalalignment = "center", horizontalalignment="center", rotation="vertical", size="small", color = 'black', weight= "semibold"  )

    ax1.legend()
    ax2.legend()
    ax1.set_ylim(550, 1100) 
    f.suptitle(f"{subfield} Volume (T1 segmentation)", fontsize=16)   
    plt.tight_layout()
    plt.show()



# for 4 graphs: Right / Left by gender
def total_hipp_vol_controls_and_patients_RL_Gender():
    f, axes = plt.subplots(2,2, sharey= True, sharex=True)
        
    sns.regplot(data=controls[controls.Gender == 'F' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'F' ], "Left"), ax=axes[0,0],color = "#d25c7e")#, lowess=True  ,color = "#ae0c20"
    sns.regplot(data=controls[controls.Gender == 'M' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'M' ], "Left"), ax=axes[1,0], color= "#a5c4f8")
    sns.regplot(data=controls[controls.Gender == 'F' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'F' ], "Right"), ax=axes[0,1],color = "#d25c7e", label="Controls Female")
    sns.regplot(data=controls[controls.Gender == 'M' ], x="Age", y=total_vol_per_side(controls[controls.Gender == 'M' ], "Right"), ax=axes[1,1], label="Controls Male", color = "#a5c4f8")


        #patients

    axes[0,0].scatter(patients[patients.Gender == 'F'][patients.Lesion == "Left"]["Age"], total_vol_per_side(patients[patients.Gender == 'F'][patients.Lesion == "Left"], "Left"), color="#ae0c20", marker="s", )
    axes[0,0].scatter(patients[patients.Gender == 'F'][patients.Lesion != "Left"]["Age"], total_vol_per_side(patients[patients.Gender == 'F'][patients.Lesion != "Left"], "Left"), color="#ae0c20") 
    axes[0,1].scatter(patients[patients.Gender == 'F'][patients.Lesion == "Right"]["Age"], total_vol_per_side(patients[patients.Gender == 'F'][patients.Lesion == "Right"], "Right") , color="#ae0c20", marker="s", label="Ipsilesional") 
    axes[0,1].scatter(patients[patients.Gender == 'F'][patients.Lesion != "Right"]["Age"], total_vol_per_side(patients[patients.Gender == 'F'][patients.Lesion != "Right"], "Right"), color="#ae0c20" , label="Contralesional") 
    axes[1,0].scatter(patients[patients.Gender == 'M'][patients.Lesion == "Left"]["Age"], total_vol_per_side(patients[patients.Gender == 'M'][patients.Lesion == "Left"], "Left"), color="blue", marker="s") 
    axes[1,0].scatter(patients[patients.Gender == 'M'][patients.Lesion != "Left"]["Age"], total_vol_per_side(patients[patients.Gender == 'M'][patients.Lesion != "Left"], "Left"), color="blue") 
    axes[1,1].scatter(patients[patients.Gender == 'M'][patients.Lesion == "Right"]["Age"], total_vol_per_side(patients[patients.Gender == 'M'][patients.Lesion == "Right"], "Right"), color="blue" , marker="s" , label = "Ipsilesional") 
    axes[1,1].scatter(patients[patients.Gender == 'M'][patients.Lesion != "Right"]["Age"], total_vol_per_side(patients[patients.Gender == 'M'][patients.Lesion != "Right"], "Right"), color="blue", label="Contralesional" ) 
        
    axes[0,0].set_xlabel("Age (year)")
    axes[0,1].set_xlabel("Age (year)")
    axes[1,0].set_xlabel("Age (year)")
    axes[1,1].set_xlabel("Age (year)")
    axes[0,0].set_ylabel("Volume (mm3)")
    axes[1,0].set_ylabel("Volume (mm3)")
    axes[0,0].set_title("Left", loc="center", fontsize=12, fontweight="bold")
    axes[0,1].set_title("Right", loc="center", fontsize=12, fontweight="bold")
    axes[0,1].legend()
    axes[1,1].legend()
    f.suptitle(f"Total Hippocampal Volume", fontsize=20)
    plt.show()



# Box plot for T1-T2 segmentations ROIs volumes comparison in controls group
def boxplot_T1_T2_ROI_comparison():
    sns.set_theme(style="whitegrid")

    T1_volumes = '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_seg-hsf_volumes.csv'
    T2_volumes = '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/HIPLAY7_mr_2022/data/hippocampus_seg-hsf_volumes_T2.csv' 
    patients_sub = {"sub-07P":"Right", "sub-13P":"Left","sub-18P": "Left","sub-19P":"Right","sub-20P":"Right","sub-32P":"Left", "sub-34P":"Right", "sub-31C" : ""}

    dataFrame = pd.concat(map(pd.read_csv, [T1_volumes, T2_volumes]),ignore_index=True)
    controls = dataFrame[~dataFrame.Subject.isin(patients_sub)]
    
    f, axes = plt.subplots(2,2, sharey=True, sharex=True)

    sns.boxplot(data=controls[controls.Gender == 'F'], x="Sequence",y=total_vol_per_side(controls[controls.Gender == 'F'], "Left"), ax=axes[0,0],hue="Sequence", palette= "rocket")#, lowess=True ,color = "#ae0c20"
    sns.boxplot(data=controls[controls.Gender == 'M'], x="Sequence",y=total_vol_per_side(controls[controls.Gender == 'M'], "Left"), ax=axes[1,0],hue="Sequence", palette= "Paired")
    sns.boxplot(data=controls[controls.Gender == 'F'], x="Sequence",y=total_vol_per_side(controls[controls.Gender == 'F'], "Right"), ax=axes[0,1],hue="Sequence", palette= "rocket")#label="Controls Female"
    sns.boxplot(data=controls[controls.Gender == 'M'], x="Sequence",y=total_vol_per_side(controls[controls.Gender == 'M'], "Right"), ax=axes[1,1],hue="Sequence", palette= "Paired") #label="Controls Male",


    axes[0,0].set_title("Left",loc="center", fontsize=12,fontweight="bold")
    axes[0,1].set_title("Right",loc="center", fontsize=12,fontweight="bold")

    f.suptitle(f"Total Volume \n", fontsize=20,linespacing = 0.5)

    axes[0,0].set_xlabel("")
    axes[0,1].set_xlabel("")
    axes[1,0].set_xlabel("")
    axes[1,1].set_xlabel("")
    axes[0,0].set_ylabel("Volume (mm3)")
    axes[1,0].set_ylabel("Volume (mm3)")


    axes[0,0].legend([],[], frameon=False)
    axes[0,1].legend([],[], frameon=False)
    axes[1,0].legend([],[], frameon=False)
    axes[1,1].legend([],[], frameon=False)

    plt.show()

