"""Set of functions that help to use fast api w/ db"""

import json
from typing import Optional, Sequence

import requests

from src.api import schemas
from src.api.models import AuctionItemUpdate
from src.common.settings.env import API_ENDPOINT


def api_call(
    method: str,
    path: str,
    endpoint: str = API_ENDPOINT,
    expected_status_codes: Sequence[int] = (200, 204),
    **kwargs,
) -> requests.models.Response:
    r = requests.request(
        method,
        f"{endpoint}/{path}",
        **kwargs,
    )
    if r.status_code not in expected_status_codes:
        raise ValueError(f"Error in API call: {r.status_code} {r.reason}")
    return r


def create_item(item: schemas.AuctionUserCreate, endpoint: str) -> int:
    r = api_call(
        "POST",
        endpoint,
        path="/auc_ext/create_item/",
        data=json.dumps(item.dict(), default=str),
    )
    return r.status_code


def read_item_by_id(id: int, endpoint: str) -> dict:
    r = api_call(
        "GET",
        endpoint,
        path="/auc_ext/item_by_id/",
        params=dict(id=id),
    )
    return r.json()


def update_item_by_id(
    new_item: AuctionItemUpdate,
    endpoint: str,
    item_id: int,
    price_increment: int = None,
) -> dict:
    headers = {
        "accept": "application/json",
        # Already added when you pass json= but not when you pass data=
        "Content-Type": "application/json",
    }
    params = {
        "item_id": item_id,
        "price_increment": price_increment,
    }
    r = api_call(
        "PUT",
        endpoint,
        path="/auc_ext/update_item_by_id",
        params=params,
        headers=headers,
        data=json.dumps(new_item.dict(), default=str),
    )
    return r.json()


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
    r = api_call(
        "PUT",
        endpoint,
        path="/auc_ext/update_item_by_id",
        params=params,
        headers=headers,
        data=json.dumps(new_item.dict(), default=str),
    )
    return r.json()


def get_user_by_username(username: str, endpoint: str) -> requests.models.Response:
    headers = {"accept": "application/json"}
    params = {"username": username}
    return api_call(
        "GET",
        endpoint,
        path="/auc_ext/user_by_username",
        params=params,
        headers=headers,
    )


def create_user(username: str, endpoint: str) -> requests.models.Response:
    headers = {"accept": "application/json"}
    json_data = {"username": username}
    return api_call(
        "PUT",
        endpoint,
        path="/auc_ext/update_item_by_id",
        headers=headers,
        json=json_data,
    )
