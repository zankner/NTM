import fetch
import numpy as np
import json
import pandas as pd
from datetime import timedelta, date
from tqdm import tqdm
import pickle
import time

csv_file = "constituents_csv.csv"

csv_read = pd.read_csv(csv_file)
#print(csv_read)

stock_symbols = csv_read.iloc[:,0]

stock_symbol_list = stock_symbols.values.tolist()
#print(stock_symbol_list)

data_list = []

print(len(stock_symbol_list))
#numpy_data = []
#final_data = np.asarray(numpy_data)

timedim = 503

numpy_data = np.empty((5, timedim, 1))

for i in tqdm(range(len(stock_symbol_list))):
    iter_parser = fetch.parse_function(stock_symbol_list[i], 'J6VF09SPJX6ORROI', date(2017, 2, 2), date(2019, 2, 4))
    download_stage = iter_parser.json_download()
    collect_stage = iter_parser.json_collect()
    for elements in collect_stage:
        if not elements:
            raise ValueError("Null List detected %s" % stock_symbol_list[i])
    if not collect_stage:
        raise ValueError("Null List detected %s" % stock_symbol_list[i])

    collect_stage_np = np.asarray(collect_stage)
    collect_stage_np = collect_stage_np.reshape((collect_stage_np.shape[0], collect_stage_np.shape[1], 1))
    if(collect_stage_np.shape != np.empty((5, timedim, 1)).shape):
        zeros = np.zeros((5, np.abs(timedim - collect_stage_np.shape[1]), 1))
        collect_stage_np = np.concatenate((zeros, collect_stage_np), axis=1)
    numpy_data = np.concatenate((numpy_data, collect_stage_np), axis=2)

print(numpy_data.shape)

np.save('data.npy', numpy_data)
