import os
import json

wd = os.getcwd()

path = os.path.join(wd, "Data")



def select_all():
    with open(f'{path}/historical_data.json') as json_data:
        data_dict = json.load(json_data)

    data_str = json.dumps(data_dict)

    return data_str


def select_subset(to_select, key_values):

    with open(f'{path}/historical_data.json') as json_data:
        data_dict = json.load(json_data)

    if to_select == '*':
        to_select = list(data_dict['feeds'][0].keys())
    else:
        to_select = [x.strip() for x in to_select.split(",")]

    key = key_values[0]

    typ = type(data_dict["feeds"][0][key])

    if typ != None:
        response = [{k:v for k,v in x.items() if k in to_select} for x in data_dict['feeds'] if x[key_values[0]]==typ(key_values[1])]

        return response
    else:
        return ""
