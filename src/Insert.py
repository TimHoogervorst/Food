## CLASSES TO INSERT RECIPES/INGREDIENTS INTO POSTGRESS

# REFERENCE PACKAGES
from .FoodDataWrapper import FoodData
from .config import FOOD_DATA_API
from .PostgressConnector import Postgress

# PIPY PACK
import pandas as pd
import functools
import numpy as np
import json


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
class BaseDataClass:
    def from_dataframe_row(self, row: pd.Series) -> None:
        for column in row.index:
            if column.lower() in [attr for attr in dir(self)]:
                setattr(self, column.lower(), row[column])

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

        # Execute the query using the Postgress class
        db.execute_query(sql, values)

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

## CLASS OF RECIPE
class Recipe(BaseDataClass):
    def __init__(self) -> None:
        self.tablename = 'development.recipes'
        self.title = None
        self.description = None
        self.cuisine = None
        self.category = None
        self.serving = None
        self.preptime = None
        self.cooktime = None
        self.difficulty = None

## CLASS OF INGREDIENT
class Ingredient(BaseDataClass):
    def __init__(self) -> None:
        self.tablename = 'development.ingredients'
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