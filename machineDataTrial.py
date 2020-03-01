import hd5_utils
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


directory = "competitionfiles"
machines = hd5_utils.get_machine_dict(directory)
f152_list = machines['M152']
arr = np.nonzero(hd5_utils.get_all_channel_data('ch_2', f152_list, directory))

plt.hist(arr, bins='auto')  # arguments are passed to np.histogram
plt.title("Histogram ch_2 (with noise reduction)")
plt.xlabel("Datapoint #")
plt.ylabel("Frequency")
plt.show()



#.value_counts()
#sns.set_style('whitegrid')
#sns.countplot(x='Datapoint',data=arr,palette='RdBu_r')
