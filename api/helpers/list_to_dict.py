from typing import List, Dict

def convert_list_to_dict(data: List[Dict]) -> Dict:
    data_clean = {}
    # We convert the list of dict to one only dict
    for item in data:
        id = item['id']
        data_clean[id] = item["json"]

    return data_clean
