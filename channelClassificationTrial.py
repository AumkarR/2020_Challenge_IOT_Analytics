import os
import pandas as pd
import numpy as np
import hd5_utils

uniq_chn = set()
directory = "competitionfiles"
classifications = {}
for filename in os.listdir(directory):
    d = {"Classification": None, "Regression": None}
    if filename.endswith(".hdf"): 
        for ch in hd5_utils.uniq_chn:
            arr = hd5_utils.get_channel_data(ch, filename, directory)
            if np.unique(arr).size != 0 and np.unique(arr).size < 10:
                d[ch] = True
            elif np.unique(arr).size >= 10:
                d[ch] = False
    classifications[filename] = d

channelClassifications = {}
for ch in hd5_utils.uniq_chn:
    listCounter = [0, 0]
    for filenames in classifications.keys():
        try: 
            if classifications[filenames][ch] == True:
                listCounter[0] += 1
            else:
                listCounter[1] += 1
        except:
            continue
    try:
        channelClassifications[ch] = listCounter
    except KeyError:
        continue

regressiveList = []    
for ch in channelClassifications:
    if channelClassifications[ch][1] > 50:
        regressiveList.append(ch)
print(regressiveList)            

            
