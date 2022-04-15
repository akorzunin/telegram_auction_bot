# %%
#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.getenv('PWD')
PWD

import sys
sys.path.insert(1, PWD)
from fake_data_seed import data_link
from random import randint
import requests
from db_api import schemas
import json

# %%
ENDPOINT = os.getenv('ENDPOINT')
ENDPOINT

# %%
from random import sample
def main():
    NUMBER_OF_ITEMS = 50
    NUMBER_OF_USERS = 10
    item_list = sample(range(1,  len(data_link.df_elden)-1), NUMBER_OF_ITEMS)
    user_list = sample(range(1,  len(data_link.df_pokemon)-1), NUMBER_OF_USERS)

    for i in user_list:
        user = data_link.df_pokemon.loc[i][0]
        # add user to db
        json_data = schemas.AuctionUserCreate(
            username=user,
        )
        r = requests.post(f'http://{ENDPOINT}:8001/auc_ext/create_user/', json=json_data.dict())
        # display(user, r.status_code)
        
    for i in item_list:
        df = data_link.df_elden.loc[i]
        item = dict(
            name=df['name'],
            description=df['description'],
            image=df['image'],
        )
        json_data = schemas.AuctionItemCreate(
            title=item['name'],
            description=item['description'],
            price=randint(1000, 10000),
            is_start_price=True,
            photo=f'{item["image"]}|{item["image"]}',
            owner_id=0,
        )
        r = requests.post(f'http://{ENDPOINT}:8001/auc_ext/create_item/', data=json.dumps(json_data.dict(), default=str))

    # display(item, r.status_code)

if __name__ == '__main__':
    main()
