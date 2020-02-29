import hd5_utils as hd
import h5py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

numArr = np.array(hd.get_channel_data('ch_0', "demo.hdf", "."))
N  = 3    # Filter order
Wn = 0.1 # Cutoff frequency
B, A = signal.butter(N, Wn, output='ba')
smooth_data = signal.filtfilt(B,A, numArr)
plt.plot(numArr,'r-')
plt.plot(smooth_data,'b-')
plt.show()

mse = np.square(numArr - smooth_data).mean()
print(mse)
print(numArr[0:10])
