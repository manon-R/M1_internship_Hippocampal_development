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

2) 
