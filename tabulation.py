import csv
import json

import pandas as pd

meta_file = 'data/meta_results.json'
applic_file = 'data/data_results.json'

with open(meta_file, 'r', encoding='utf8') as f:
    meta_data = json.load(f)
with open(applic_file, 'r', encoding='utf8') as f:
    applic_data = json.load(f)

meta_data = {item['Contract_ID']: item for item in meta_data if 'Contract_ID' in item}
applic_data = {item['contract_id']: item for item in applic_data if 'contract_id' in item}

glob_tags = {
    'tag_construction',
    'tag_energy_not_nuclear',
    'tag_nuclear power',
    'tag_electronics_supply_installation',
    'tag_materials_supplies',
    'tag_equipment_supply_installation',
    'tag_research_design_works',
    'tag_chemical_production',
    'tag_other_services',
}


def cleanup_name(text):
    return text.replace('"', '').replace("'", '').replace("\t", ' ').replace("«", '').replace("»", '').strip()


def cleanup_price(text):
    text = text.rsplit(' ', 1)[0].rsplit('.', 1)[0].replace(",", '')
    text = text.lower().replace('cny', '').replace('rmb', '').replace('¥', '').replace('$', '').replace('€', '')
    return text.strip()


companies = {}
contracts = {}

for contract_id, data in meta_data.items():
    if contract_id in applic_data:
        data.update(applic_data[contract_id])
    participating_company = cleanup_name(data['Name_of_the_participating_company'])
    if participating_company not in companies:
        companies[participating_company] = {
            'name': participating_company,
            'parent': None,
            'is_participant': 1,
            'is_customer': 0,
        }
    else:
        companies[participating_company]['is_participant'] = 1

    customer_company = data['Customer_company/agent'].split('@')
    if len(customer_company) == 2:
        customer_company, customer_company_parent = customer_company
        customer_company = cleanup_name(customer_company)
        customer_company_parent = cleanup_name(customer_company_parent.split('(')[-1].split(')')[0])

        if customer_company not in companies:
            companies[customer_company] = {
                'name': customer_company,
                'parent': customer_company_parent,
                'is_participant': 0,
                'is_customer': 1,
            }
        else:
            companies[participating_company]['is_customer'] = 1
        if customer_company_parent not in companies:
            companies[customer_company_parent] = {
                'name': customer_company_parent,
                'parent': None,
                'is_participant': 0,
                'is_customer': 0,
            }

    bidding_company = data['Bidding_company/agent'].split('@')
    if len(bidding_company) == 2:
        bidding_company, bidding_company_parent = bidding_company
        bidding_company = cleanup_name(bidding_company)
        bidding_company_parent = cleanup_name(bidding_company_parent.split('(')[-1].split(')')[0])

        if bidding_company not in companies:
            companies[bidding_company] = {
                'name': bidding_company,
                'parent': bidding_company_parent,
                'is_participant': 0,
                'is_customer': 1,
            }
        else:
            companies[participating_company]['is_customer'] = 1
        if bidding_company_parent not in companies:
            companies[bidding_company_parent] = {
                'name': bidding_company_parent,
                'parent': None,
                'is_participant': 0,
                'is_customer': 0,
            }

    start_date = data.get('contract_start_date')
    if start_date == 'n/a':
        start_date = None
    deadline_date = data.get('contract_deadline_date')
    if deadline_date == 'n/a':
        deadline_date = None

    for tag in glob_tags:
        if tag in data:
            if data[tag] not in ('0', '1'):
                del data[tag]
            else:
                data[tag] = int(data[tag])
    try:
        price = int(cleanup_price(data['Price']))
    except:
        price = None

    contracts[contract_id] = {
        'contract_id': contract_id,
        'subject': data['Subject'],
        'summary': data.get('contrtact_short_summary', None),
        'publication_date': data['Contract_date'],
        'start_date': start_date,
        'deadline_date': deadline_date,
        'place': data.get('contract_geo'),
        'price': price,
        'participating_company': participating_company,
        'customer_agent_company': customer_company,
        'bidding_agent_company': bidding_company,

        'tag_construction': data.get('tag_construction', None),
        'tag_energy_not_nuclear': data.get('tag_energy_not_nuclear', None),
        'tag_nuclear_power': data.get('tag_nuclear power', None),
        'tag_electronics_supply/installation': data.get('tag_electronics_supply_installation', None),
        'tag_materials_supplies': data.get('tag_materials_supplies', None),
        'tag_equipment_supply/installation': data.get('tag_equipment_supply_installation', None),
        'tag_research/design': data.get('tag_research_design_works', None),
        'tag_chemical_production': data.get('tag_chemical_production', None),
        'tag_other_services': data.get('tag_other_services', None),
    }

with open('contracts.json', 'w', encoding='utf8') as f:
    json.dump(list(contracts.values()), f)
with open('companies.json', 'w', encoding='utf8') as f:
    json.dump(list(companies.values()), f)

contracts_df = pd.read_json('contracts.json')

for param in ('start_date', 'publication_date', 'deadline_date'):
    contracts_df[param] = pd.to_datetime(contracts_df[param], format='%Y-%m-%d', errors='coerce')

with open('contracts_cl.json', 'w', encoding='utf8') as f:
    f.write(contracts_df.to_json(orient='records'))
contracts_df.to_csv('contracts_cl.csv', sep='\t', quoting=csv.QUOTE_ALL)

companies_df = pd.read_json('companies.json')
companies_df.to_csv('companies.csv', sep='\t', quoting=csv.QUOTE_ALL)
