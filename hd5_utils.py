import h5py
import os
import pandas as pd
import numpy as np
from scipy import signal

cont_chs = ['ch_7', 'ch_180', 'ch_248', 'ch_124', 'ch_49', 'ch_110', 'ch_218', 
'ch_102', 'ch_60', 'ch_361', 'ch_33', 'ch_291', 'ch_258', 'ch_295', 'ch_42', 
'ch_65', 'ch_50', 'ch_21', 'ch_177', 'ch_306', 'ch_179', 'ch_121', 'ch_26', 
'ch_288', 'ch_74', 'ch_57', 'ch_114', 'ch_46', 'ch_129', 'ch_207', 'ch_285', 
'ch_265', 'ch_256', 'ch_192', 'ch_185', 'ch_1', 'ch_135', 'ch_113', 'ch_61', 
'ch_96', 'ch_117', 'ch_273', 'ch_318', 'ch_196', 'ch_4', 'ch_376', 'ch_35', 
'ch_322', 'ch_79', 'ch_36', 'ch_99', 'ch_5', 'ch_25', 'ch_157', 'ch_305', 
'ch_137', 'ch_130', 'ch_299', 'ch_98', 'ch_88', 'ch_127', 'ch_205', 'ch_52', 
'ch_70', 'ch_187', 'ch_225', 'ch_167', 'ch_375', 'ch_307', 'ch_87', 'ch_66', 
'ch_68', 'ch_44', 'ch_91', 'ch_348', 'ch_51', 'ch_80', 'ch_55', 'ch_266', 
'ch_126', 'ch_90', 'ch_56', 'ch_47', 'ch_38', 'ch_297', 'ch_178', 'ch_27', 
'ch_9', 'ch_138', 'ch_172', 'ch_48', 'ch_109', 'ch_37', 'ch_134', 'ch_106', 
'ch_119', 'ch_13', 'ch_11', 'ch_72', 'ch_226', 'ch_257', 'ch_323', 'ch_63', 
'ch_62', 'ch_125', 'ch_10', 'ch_14', 'ch_24', 'ch_59', 'ch_43', 'ch_294', 
'ch_54', 'ch_188', 'ch_194', 'ch_64', 'ch_95', 'ch_111', 'ch_41', 'ch_161', 
'ch_31', 'ch_58', 'ch_208', 'ch_206', 'ch_156', 'ch_339', 'ch_30', 'ch_53', 
'ch_173', 'ch_255', 'ch_308', 'ch_39', 'ch_84', 'ch_40', 'ch_133', 'ch_341', 
'ch_105', 'ch_67', 'ch_75', 'ch_32', 'ch_163', 'ch_69', 'ch_93', 'ch_283', 
'ch_170', 'ch_274', 'ch_343', 'ch_316']

day_d = dict()
directory = "competitionfiles"
for file in os.listdir(directory):
    try:
        day_d[file.split('_')[1]].append(file)
    except KeyError:
        day_d[file.split('_')[1]] = [file]

uniq_chn = set()
for filename in os.listdir(directory):
    f = h5py.File(os.path.join(directory, filename), 'r')
    for ch_name in f['DYNAMIC DATA']:
        uniq_chn.add(ch_name)
uniq_chn = list(uniq_chn)

def hd5_to_df(filename, directory, resample=False):
    if filename.endswith(".hdf"):
        f = h5py.File(os.path.join(directory, filename), 'r')
        d = dict()
        for key, item in f['DYNAMIC DATA'].items():
            d[key] = np.array(item['MEASURED'])
            df = pd.DataFrame(d)

        first_ts = f['DYNAMIC DATA'].attrs['FIRST ACQ TIMESTAMP']
        second_ts = f['DYNAMIC DATA'].attrs['LAST ACQ TIMESTAMP']
        dts = pd.to_datetime(first_ts.decode("utf-8"))
        dtf = pd.to_datetime(second_ts.decode("utf-8"))

        ts = np.linspace(dts.value, dtf.value, len(f['DYNAMIC DATA']['ch_1']['MEASURED']))
        ts_ind = pd.to_datetime(ts)
        df = df.set_index(ts_ind)

    for name in uniq_chn:
        if name not in df.columns:
            df[name] = np.NaN

    if resample:
        df = df.resample('1s').mean()
    return df

def get_channel_data(ch_name, filename, directory):
    if filename.endswith(".hdf"):
        f = h5py.File(os.path.join(directory, filename), 'r')
        if ch_name not in f['DYNAMIC DATA']: return np.array([])
        return np.array(f['DYNAMIC DATA'][ch_name]['MEASURED'])
    else:
        print('Invalid Filename')
        return None

def get_channel_df(ch_name, filename, directory):
    if filename.endswith(".hdf"):
        f = h5py.File(os.path.join(directory, filename), 'r')
        if ch_name not in f['DYNAMIC DATA']: return np.array([])
        first_ts = f['DYNAMIC DATA'].attrs['FIRST ACQ TIMESTAMP']
        second_ts = f['DYNAMIC DATA'].attrs['LAST ACQ TIMESTAMP']
        dts = pd.to_datetime(first_ts.decode("utf-8"))
        dtf = pd.to_datetime(second_ts.decode("utf-8"))

        ts = np.linspace(dts.value, dtf.value, len(f['DYNAMIC DATA']['ch_1']['MEASURED']))
        ts_ind = pd.to_datetime(ts)
        df = pd.DataFrame({"ch_name": np.array(f['DYNAMIC DATA'][ch_name]['MEASURED'])}, index=ts_ind)
        return df

    else:
        print('Invalid Filename')
        return None

def get_all_channel_data(ch_name, file_list, directory):
    channel_data = []
    for filename in file_list:
        if filename.endswith(".hdf"):
            channel_data.extend(list(get_channel_data(ch_name, filename, directory)))
    return np.array(channel_data)

def get_machine_dict(directory):
    categ = {}
    for filename in os.listdir(directory):
        f = h5py.File(os.path.join(directory, filename), 'r')
        chanIDs = f['DYNAMIC DATA']
        currLen = len(chanIDs.keys())
        if currLen == 152 or currLen == 120 or currLen == 238:
            try:
                if categ['M' + str(currLen)] != None:
                    categ['M' + str(currLen)].append(filename)
                else:
                    categ['M' + str(currLen)] = [filename]
            except KeyError:
                categ['M' + str(currLen)] = [filename]

    return categ

def get_day_df(day, ch_name, directory):
    day_l = list(day_d.keys())[day]
    df = get_channel_df(ch_name, day_d[day_l][0], directory)
    if len(day_d[day_l]) == 1:
        df = df['ch_name']
        df.to_numpy()
        return df[1:]
    
    for _file in day_d[day_l][1:]:
        pdf = get_channel_df(ch_name, _file, directory)
        df = pd.concat([df, pdf], axis=0)
    
    pdf = df['ch_name']
    df = df.rolling(10).mean()[::10]
    print(np.nonzero(df))
    return df

def get_min_channel(ch_name, directory):
    files = [filename for filename in os.listdir(directory)]
    return [get_channel_data(ch_name, file, directory).min() for file in files]

def get_max_channel(ch_name, directory):
    files = [filename for filename in os.listdir(directory)]
    return [get_channel_data(ch_name, file, directory).max() for file in files]

def get_avg_channel(ch_name, directory):
    files = [filename for filename in os.listdir(directory)]
    return [get_channel_data(ch_name, file, directory).mean() for file in files]

def get_day_number(day):
    return list(day_d.keys()).index(day)

