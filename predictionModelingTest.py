from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import hd5_utils
import os
import pandas

directory = "competitionfiles"
lm = LinearRegression()
for filename in os.listdir(directory):
    if filename.endswith(".hdf"):
        for ch in hd5_utils.uniq_chn:
            tempArr = hd5_utils.get_channel_df(ch, filename, directory)
            if len(tempArr) == 0: continue
            for time in tempArr.index:
                x_train, x_test, y_train, y_test = train_test_split(time, hd5_utils.get_channel_data(ch, filename, directory), test_size=0.2)
                lm.fit(x_train, y_train)
                print(lm.intercept_)
                
# get the first timestamp of the file
# subtract the time in the loop from the first timestamp
# Convert that time difference to a float use the float as the time variable
