import hd5_utils
import matplotlib.pyplot as plt

directory = "competitionfiles"
machines = hd5_utils.get_machine_dict(directory)
f152_list = machines['M152']
plt.plot(hd5_utils.get_all_channel_data('ch_2', f152_list, directory))