# %%
import json

# %%
from random import randint, sample

import requests
from fake_data_seed import data_link

from db_api import schemas

# %%
from settings.env import API_ENDPOINT as ENDPOINT


def main():
    NUMBER_OF_ITEMS = 50
    NUMBER_OF_USERS = 10
    item_list = sample(range(1, len(data_link.df_elden) - 1), NUMBER_OF_ITEMS)
    user_list = sample(range(1, len(data_link.df_pokemon) - 1), NUMBER_OF_USERS)

    for i in user_list:
        user = data_link.df_pokemon.loc[i][0]
        # add user to db
        json_data = schemas.AuctionUserCreate(
            username=user,
        )
        _ = requests.post(
            f"{ENDPOINT}/auc_ext/create_user/", json=json_data.model_dump()
        )
        # display(user, r.status_code)

    for i in item_list:
        df = data_link.df_elden.loc[i]
        item = dict(
            name=df["name"],
            description=df["description"],
            image=df["image"],
        )
        json_data = schemas.AuctionItemCreate(
            title=item["name"],
            description=item["description"],
            price=randint(1000, 10000),
            is_start_price=True,
            photo=f'{item["image"]}|{item["image"]}',
            owner_id=0,
        )
        _ = requests.post(
            f"{ENDPOINT}/auc_ext/create_item/",
            data=json.dumps(json_data.dict(), default=str),
        )

    # display(item, r.status_code)


if __name__ == "__main__":
    main()
