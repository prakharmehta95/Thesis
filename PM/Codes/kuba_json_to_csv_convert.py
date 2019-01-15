import json
from pprint import pprint
import os
import pandas as pd

data_folder = r'C:\Users\iA\Desktop\New folder'

for file in os.listdir(data_folder):
    if os.path.splitext(file)[1] == '.json':
        file_name = os.path.splitext(file)[0]
        with open(os.path.join(data_folder, file)) as data_file:
            data=json.load(data_file)
        data_df = pd.DataFrame(data=None)
        for key in data.keys():
            data_df[key] = data[key]
        data_df.to_csv(os.path.join(data_folder, file_name+'.csv'))


