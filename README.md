# M1_internship_Hippocampal_development


******* Overview *******

In this folder you will find both python scripts ("scripts" folder) allowing:

- Data extraction and estimation of ROI volumes in mm³ from the segmentation (HSF) of T1 and T2 recombined images.

-  Data extraction and estimation of the average R1 rate of each ROI based on either T1 segmentation + R1 map or T2 segmentation (placed in T1 space) + R1 map

- Graphical representation of the 2 metrics: volumes and R1 (according to age)

- Statistical analyses

and also csv files to store computation of both volumes and average R1 rate of each subfield.
Note: "Lesion" and "Sequence" columns were added manually.

All of these files were used to perform an exploratory study of the hippocampal subfields using 7T MRI : Normative development and TLE patients during adolescence


******* Python scripts *******

1) To extract and estimate the ROI volumes of the T1 and / or T2 segmentations, use the script : compute_T1-T2_ROIs_volumes.py

Depending on the DIRECTORY_NAME used, you can extract and estimate T1 or T2 ROIs volumes. The program allows you to retrieve and store in a csv file the following data:
Subject, Age, Gender, DG-Left, CA1-Left, CA2-Left, CA3-Left, Subiculum-Left, DG-Right, CA1-Right, CA2-Right, CA3-Right, Subiculum-Right

Additional code left as a comment at the end of the file allows the combined CA2 + CA3 volumes to be calculated directly.

2) To extract and estimate the average R1 rate of each ROI based on either T1 segmentation + R1 map or T2 segmentation (placed in T1 space) + R1 map use the script : R1_from_T1-T2_ROIs.py

* To extract R1 rate from T1 segmentation call the function : retrieve_R1_T1()
This function allows you to retrieve and store in a csv file the following data for T1 segmentation:
Subject, Age, Gender, DG-Left, CA1-Left, CA2-Left, CA3-Left, Subiculum-Left, DG-Right, CA1-Right, CA2-Right, CA3-Right, Subiculum-Right


* To extract R1 rate from T2 segmentation call the function : retrieve_R1_T2()
The program allows you to retrieve and store in a csv file the following data for T2 segmentation:
Subject, Age, Gender, DG, CA1, CA2, CA3, Subiculum

Please note that to extract R1 from T2 segmentation we need to registrate T2 in T1 space using the shell script : '/neurospin/grip/protocols/MRI/HIPLAY7_LHP_2016/Scripts/2022-06-02_T1w_to_T2w_registration_yl.sh'.(Ants library) This script allows to obtain bilateral T2 segmentation in T1 space (therefore in R1 map space)  

3) To generate graphical representations of R1 rates as a function of age use the script : R1_graphs. This program offers 3 charts format through 3 different functions: 

- plot_total_hipp_R1_RL_controls() => 1 figure, 2 subplots (Right / Left) of total hippocampal average R1 for control group. Female and Male plots are represented

- plot_hipp_R1_subfield_controls_patients(subfield : string) => 1 figure, 2 subplots (Right / Left)  with graphical representation of male/female curves as well as Ipsi and Contra distinction for TLE patients.

- plot_R1_hist_per_subfield(subfield : string, side: string) this function generates the histogram of R1 values for each subfield, right and left side.


Please note that for R1 rate computed from T2 ROIs, as we obtained bilateral segmentation we don't have Right / Left figure

4) To generate graphical representations of R1 rates as a function of age use the script : volumes_graphs.py. This program offers 5 charts format through 5 different functions: 

-  plot_total_hipp_volumes_control() => 1 figure, 2 subplots (Male / Female) of total hippocampal volumes for control group. 

- plot_hipp_volumes_RL_control() => 1 figure, 2 subplots (Right / Left) of total hippocampal volumes for control group. Female and Male curves are represented.

- plot_volumes_per_subfield(subfield : string) => 1 figure, 2 subplots (Male / Female) of hippocampal volumes per subfield for control and patient group, with Ipsi and Contra distinction for TLE patients.

- total_hipp_vol_controls_and_patients_RL_Gender() => 1 figure, 4 subplots : lines Female / Male, columns Left / Right of total hippocampal volumes for control and patient group, with Ipsi and Contra distinction for TLE patients.

- boxplot_T1_T2_ROI_comparison() => 1 figure, 4 subplots (boxplots) : lines Female / Male, columns Left / Right of  hippocampal volumes for control group to compare computation from T1 and T2 ROIs segmentation.

5) To perform distribution normality tests, ttest and correlation tests use the script : stats.py
(Pingouin library)

******* Csv files *******

In "data" forlder we stored 4 csv files, for each file we automatically stored the following informations: Subject, Age, Gender, and manually added Lesion and Sequence informations. 

1) hippocampus_R1.csv => Store R1 average rate for each hippocampal subfield from T1 ROIs (Right and Left of subfield see variable SUBFIELDS) from subject 03C to subject 34P (without 31C and 33C subjects see "Unresolved" section)

2) hippocampus_R1_T2.csv => Store R1 average rate for each hippocampal subfield  from T2 ROIs (Bilateral segmentation of subfield see variable SUBFIELDS) from subject 03C to subject 30C (without 31C, 32P, 33C and 34P subjects see "Unresolved" section)

3) hippocampus_seg-hsf_volumes.csv => Store hippocampal volumes for each subfield from T1 ROIs (Right and Left of subfield see variable SUBFIELDS) from subject 03C to subject 34P (without 31C and 33C subjects see "Unresolved" section)

4) hippocampus_seg-hsf_volumes_T2.csv => Store hippocampal volumes for each  subfield  from T2 ROIs (Right and Left of subfield see variable SUBFIELDS) from subject 03C to subject 30C (without 31C, 32P, 33C and 34P subjects see "Unresolved" section)

Please note: 
The subjects 00C, 01C, 02C are pilots


******* Unresolved *******

* Problem of subject nomenclatures : 
Absence of subject 31C ?
Problem with the naming of subject td 220 234 (33rd or 34th acquisition?)
Problem of T2 registration from subject 32 which leads to the absence of recombined T2 from 32P to 34P
See file "liste_anonyme.xls" to compare the different nomenclatures used


* Pb sub-34P folder T1seg-hsf : 
Content differs from other subjects for "T1seg-hsf" : "hsf_outputs" folder and T1w + T2w (Right / Left) segmentations in the same folder

