import os
import json

wd = os.getcwd()

path = os.path.join(wd, "Data")

def insert_obs(columns, values):

    with open(f'{path}/historical_data.json') as json_data:
        data_dict = json.load(json_data)

    to_insert = {k:v for k, v in zip(columns, values)}

    data_dict['feeds'].append(to_insert)

    data_dict["totalFeed"] +=1

    # Directly from dictionary
    with open(f'{path}/historical_data.json', 'w') as outfile:
        json.dump(data_dict, outfile)

    return to_insert
