import json

import requests
from tqdm import tqdm

from common import base_prompt_data, base_prompt_meta
from common import cleanup, llm_params
from common import url, headers

ds_path = './atomic/ds/'
data_file = 'all_applic.dat'
meta_file = 'all_meta.dat'
delimiter = '*$*'

with open(ds_path + meta_file, 'r', encoding='utf8') as f:
    meta_items = cleanup(f.read()).split(delimiter)
with open(ds_path + data_file, 'r', encoding='utf8') as f:
    data_items = cleanup(f.read()).split(delimiter)

meta_keys = {
    'Contract date',
    'Contract ID',
    'Subject',
    'Name of the participating company',
    'Price',
    'Customer company/agent',
    'Bidding company/agent'
}


def validate_result_meta(text):
    validated_data = {}
    for row in text.split('\n'):
        key = row.split(':', 1)[0]
        if key in meta_keys:
            validated_data[key] = row
    if len(validated_data) == len(meta_keys):
        return text
    else:
        return None


data_keys = {
    'contract_id',
    'contract_short_summary',
    'contract_start_date',
    'contract_deadline_date',
    'contract_geo',
    'tag_construction',
    'tag_energy_not_nuclear',
    'tag_nuclear power',
    'tag_electronics_supply_installation',
    'tag_materials_supplies',
    'tag_equipment_supply_installation',
    'tag_research_design_works',
    'tag_other_services',
    'tag_chemical_production'
}


def validate_result_data(text):
    validated_data = {}
    for row in text.split('\n'):
        row = row.split(':', 1)
        if len(row) == 1:
            continue
        key, value = row
        key = key.strip()
        if key in data_keys and key not in validated_data:
            validated_data[key] = value.strip().split('\n', 1)[0]
    return validated_data


meta_results = []
for item in tqdm(meta_items):
    item = item.strip()
    if len(item) < 50:
        continue
    data = llm_params.copy()
    data['messages'] = [{"role": "user", "content": base_prompt_meta + item}]
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        result = response.json().get('choices', [])[0].get('message', {}).get('content')
        if result and validate_result_meta(result):
            meta_results.append(result)

with open('meta_results.json', 'w', encoding='utf8') as f:
    json.dump(meta_results, f)

data_results = []
for item in tqdm(data_items):
    item = item.strip()
    if len(item) < 50:
        continue
    data = llm_params.copy()
    data['messages'] = [{"role": "user", "content": base_prompt_data + item}]
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        result = response.json().get('choices', [])[0].get('message', {}).get('content')
        if result and validate_result_data(result):
            data_results.append(result)

with open('data_results.json', 'w', encoding='utf8') as f:
    json.dump(data_results, f)
