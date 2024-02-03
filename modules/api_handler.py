"""Set of functions that help to use fast api w/ db"""

# %%
import requests
import json

# load .env variables
import os
from dotenv import load_dotenv

load_dotenv()
PWD = os.getenv("PWD")

import sys

sys.path.insert(1, PWD)

from db_api import schemas


# %%
def create_item(item: schemas.AuctionUserCreate, endpoint: str) -> int:

    r = requests.post(
        url=f"http://{endpoint}:8001/auc_ext/create_item/",
        data=json.dumps(item.dict(), default=str),
    )

    return r.status_code


def read_item_by_id(id: int, endpoint: str) -> dict:

    r = requests.get(
        url=f"http://{endpoint}:8001/auc_ext/item_by_id/",
        params=dict(id=id),
    )

    return r.json()


def update_item_by_id(
    new_item: schemas.AuctionItemUpdate,
    endpoint: str,
    item_id: int,
    price_increment: int = None,
) -> int:

    headers = {
        "accept": "application/json",
        # Already added when you pass json= but not when you pass data=
        "Content-Type": "application/json",
    }

    params = {
        "item_id": item_id,
        "price_increment": price_increment,
    }

    r = requests.put(
        url=f"http://{endpoint}:8001/auc_ext/update_item_by_id/",
        headers=headers,
        params=params,
        data=json.dumps(new_item.dict(), default=str),
    )

    return r.json()


# %%
# def add_item_to_user(item_id: int, user_id: int, endpoint: str):

#     pass


def reassign_item(
    item_id: int, user_id: int, endpoint: str, price_increment: int = None
) -> dict:

    new_item = schemas.AuctionItemUpdate(
        owner_id=user_id,
    )

    headers = {
        "accept": "application/json",
        # Already added when you pass json= but not when you pass data=
        "Content-Type": "application/json",
    }

    params = {
        "item_id": item_id,
        "price_increment": price_increment,
    }

    r = requests.put(
        url=f"http://{endpoint}:8001/auc_ext/update_item_by_id/",
        headers=headers,
        params=params,
        data=json.dumps(new_item.dict(), default=str),
    )

    return r.json()


#  %%


def get_user_by_username(username: str, endpoint: str) -> requests.models.Response:
    headers = {
        "accept": "application/json",
    }

    params = {
        "username": username,
    }

    return requests.get(
        f"http://{endpoint}:8001/auc_ext/user_by_username/",
        headers=headers,
        params=params,
    )


def create_user(username: str, endpoint: str) -> requests.models.Response:
    headers = {
        "accept": "application/json",
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        "username": username,
    }

    return requests.post(
        f"http://{endpoint}:8001/auc_ext/create_user/", headers=headers, json=json_data
    )


# %%
if __name__ == "__main__":
    endpoint = "192.168.1.125"
    from random import randint

    # test create_item
    item = schemas.AuctionItemCreate(
        title=f"item_from_telegram{str(randint(0, 10**10))}",
        price=200,
        photo="123|123",
        owner_id=0,
    )

    create_item(
        item=item,
        endpoint=endpoint,
    )

# %%
