import h5py
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
​
directory = "competitionfiles"
for filename in os.listdir(directory):
    if filename.endswith(".hdf"):
        f = h5py.File(os.path.join(directory, filename), 'r')
        chanIDs = f['DYNAMIC DATA']
        ChannelName = 'ch_0'
        k = chanIDs.keys()
        for x in k:
            m = mean(list(k[x]['MEASURED']))
            sd = pstdev(np.array[k[x]['MEASURED']])
            nsd = m + 3 * sd
            if k[x]['MEASURED'] > nsd
                .drop(index = k[x]['MEASURED'])
        break
    else:
        continue
