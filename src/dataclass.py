## CLASSES TO INSERT RECIPES/INGREDIENTS INTO POSTGRESS

# REFERENCE PACKAGES
from .FoodDataWrapper import FoodData
from .PostgressConnector import Postgress

# PIPY PACK
import pandas as pd
import functools
import numpy as np
import json
import re
from typing import Any, Dict, Union, List


## Wrapper functions
def clean_data(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):

        for attr in self.__dict__:
            value = getattr(self, attr)
            
            if isinstance(value, (np.int64, np.float64)):                               # Convert to float
                setattr(self, attr, value.item())
            elif isinstance(value, pd.Timestamp):                                       # convert to proper timestamp
                setattr(self, attr, value.to_pydatetime())
            elif isinstance(value, pd.Series):                                          # convert to single value
                setattr(self, attr, value.values[0])
            elif isinstance(value, dict):                                               # convert to json
                json_value = json.dumps(value)
                setattr(self, attr, json_value)
            elif isinstance(value, list) and all(isinstance(i, dict) for i in value):   # convert list to json
                json_value = json.dumps(value)
                setattr(self, attr, json_value)
            
            if value in ['', None]:
                setattr(self, attr, None)
        
        return func(self, *args, **kwargs)
    return wrapper

## Base class for populating attributes from a DataFrame row
class DataClassBase:

    attribute_mapping: Dict[str, Union[str, List[str]]] = {}

    def from_dataframe_row(self, row: pd.Series) -> None:
        self._populate_from_source(row.to_dict())

    def from_json(self, json_data: Union[Dict[str, Any], str]) -> None:
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        self._populate_from_source(json_data)

    def _populate_from_source(self, source: Dict[str, Any]) -> None:
        attr_map = {self._normalize(attr): attr for attr in dir(self) if not attr.startswith('_')}
        
        reverse_map = {}
        for attr, keys in self.attribute_mapping.items():
            if isinstance(keys, list):
                for key in keys:
                    reverse_map[self._normalize(key)] = attr
            else:
                reverse_map[self._normalize(keys)] = attr

        for key, value in source.items():
            normalized_key = self._normalize(key)
            
            if normalized_key in reverse_map:
                attr_name = reverse_map[normalized_key]
                setattr(self, attr_name, value)
            elif normalized_key in attr_map:
                setattr(self, attr_map[normalized_key], value)
            else:
                print(f"Warning: No matching attribute found for '{key}'")

    def _normalize(self, name: str) -> str:
        # Convert to lowercase and remove non-alphanumeric characters for comparison
        return re.sub(r'\W', '', name).lower()

    @clean_data
    def save_to_db(self, db: Postgress) -> None:
        table_name = getattr(self, 'tablename', None)
        if not table_name:
            raise ValueError("Table name not specified in the class")

        columns = []
        values = []
        for column, value in self.__dict__.items():
            if column != 'tablename' and value is not None:
                columns.append(column)
                values.append(value)

        # Create the SQL query
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        db.execute_query(sql, values)

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

## CLASS OF RECIPE
class Recipe(DataClassBase):

    attribute_mapping = {
        'steps': ['list_of_steps', 'list of steps', 'step'],
        'title': ['name', 'recipe_name', 'recipe name'],
        'servings': ['serving', 'amount'],
        'ingredients': ['list_of_ingredients', 'list of ingredients']
    }

    def __init__(self) -> None:
        self.tablename = 'datamodel.recipes'
        self.title = None
        self.description = None
        self.cuisine = None
        self.category = None
        self.servings = None
        self.preptime = None
        self.cooktime = None
        self.difficulty = None
        self.steps = None
        self.ingredients = None

## CLASS OF INGREDIENT
class Ingredient(DataClassBase):
    def __init__(self) -> None:
        self.tablename = 'datamodel.ingredients'
        self.fdcid = None
        self.description = None
        self.datatype = None
        self.brandowner = None
        self.marketcountry = None
        self.modifieddate = None
        self.foodcategory = None
        self.datasource = None
        self.servingsizeunit = None
        self.servingsize = None
        self.score = None
        self.microbes = None
        self.foodmeasures = None
        self.foodnutrients = None




def get_ingredients(ingredients: list, db: Postgress, fd: FoodData):
    for ingredient in ingredients:
        get_ingredient(ingredient, db, fd)

def get_ingredient(inregrient: str, db: Postgress, fd: FoodData):
    response = fd.search(inregrient, limit=1)
    df = fd.to_df(response, 'foods')
    ingredient = Ingredient()
    ingredient.from_dataframe_row(df.iloc[0])
    ingredient.save_to_db(db)