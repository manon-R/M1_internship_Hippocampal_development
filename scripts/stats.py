import os
import ants
import numpy as np
import pandas as pd
import csv
import pingouin as pg


#Refaire code stat normality, ttest et correlation

""" all_controls_volumes_T2 = total_hipp_volume(controls)/2
all_controls_volumes_T1 = total_hipp_volume(controls)/2



cf boxplot.py
dF = dataFrame[dataFrame.Subject != "sub-32P"]

    controls_T1 = total_vol_per_side(controls[controls.Sequence == "T1"],"Right")
    controls_T2 = total_vol_per_side(controls[controls.Sequence == "T2"],"Right")
    all_T1 = total_vol_per_side(dF[dF.Sequence == "T1"],"Right")
    all_T2 = total_vol_per_side(dF[dF.Sequence == "T2"],"Right")

print(pg.ttest(all_T1_right, all_T2_right, paired=True))

#p-value controls right = 1e⁻⁶

#p-value controls left = 4.58e⁻⁷
 """