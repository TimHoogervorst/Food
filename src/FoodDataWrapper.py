import requests
from config import FOOD_DATA_API
import json
import pandas as pd

class FoodData():
    def __init__(self, api_key = FOOD_DATA_API) -> None:
        self.API_KEY = api_key

    def search(self, item: str, limit=1) -> dict:
        url = f'https://api.nal.usda.gov/fdc/v1/foods/search/?api_key={self.API_KEY}'
        headers = {'Content-Type': 'application/json'}
        data = {"pageSize": limit,
                "query": item}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def get(self, fdcId:str) -> json:
        url = f'https://api.nal.usda.gov/fdc/v1/food/{fdcId}?api_key={self.API_KEY}'
        responses = requests.get(url)
        return json.loads(responses.text)

    def search_bulk(self, items:list, limit=1):
        return [self.search(item, limit) for item in items]

    def get_bluk(self, items:list):
        return [self.get(item) for item in items]

    def to_df(self, data, col) -> pd.DataFrame:
        if col:
            if isinstance(data, list):
                data = [item[col] for item in data if col in item]
            elif isinstance(data, dict) and col in data:
                data = data[col]
            else:
                raise ValueError(f"The specified column '{col}' was not found in the data.")
        
        if isinstance(data, list):
            df = pd.json_normalize(data)
        elif isinstance(data, dict):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Input data must be a dictionary or a list of dictionaries.")
        return df
    
    def to_bulk_df(self, data_list, col):
        all_data = []
        for data in data_list:
            if col:
                if isinstance(data, dict) and col in data:
                    data = data[col]
                elif isinstance(data, list):
                    data = [item[col] for item in data if col in item]
                else:
                    raise ValueError(f"The specified column '{col}' was not found in the data.")
            
            if isinstance(data, dict):
                all_data.append(data)
            elif isinstance(data, list):
                all_data.extend(data)
            else:
                raise ValueError("Each item in data_list must be a dictionary or a list of dictionaries.")
        
        return pd.json_normalize(all_data)

if __name__ == '__main__':
    client = FoodData()
    response = client.search('Butter', limit=1)
    df = client.to_df(response, 'foods')
    print('Working Corectly ... ')