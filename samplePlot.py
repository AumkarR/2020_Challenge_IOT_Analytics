import hd5_utils
import matplotlib.pyplot as plt
import numpy as np
import os
import h5py
import pandas as pd

directory = "competitionfiles"
machines = hd5_utils.get_machine_dict(directory)
for filename in os.listdir(directory):
    if filename.endswith(".hdf"): 
        f = h5py.File(os.path.join(directory, filename), 'r')
        chanIDs = f['DYNAMIC DATA']
        df = pd.DataFrame.from_dict(f['DYNAMIC DATA'])
        print(df.head(10))
        break
    else:
        continue
f152_list = machines['M152']
arr = np.nonzero(hd5_utils.get_all_channel_data('ch_2', f152_list, directory))

#plt.plot(arr)
for x in arr:
    print(x)

plt.plot(arr[0])