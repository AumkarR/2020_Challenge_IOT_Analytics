import hd5_utils as hd
import h5py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

numArr = np.array(hd.get_channel_data('ch_0', "demo.hdf", "."))
rat = pd.Series(numArr).rolling(window = 7).mean()
rat.plot(style = 'k')

mse = np.square(numArr - rat).mean()
print(mse)
print(numArr[0:10])
