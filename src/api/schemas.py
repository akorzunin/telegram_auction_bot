from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel


class AuctionItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    is_start_price: bool
    photo: str
    owner_id: int
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now() + relativedelta(years=1)


class AuctionItemCreate(AuctionItemBase):
    """Create item from API data and save it to database"""

    is_start_price: bool = True


class AuctionItemRead(AuctionItemBase):
    """Read item from database"""

    id: int
    is_sold: bool
    end_date: datetime

    class Config:
        orm_mode = True


class AuctionItemUpdateReq(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    is_start_price: Optional[bool] = False
    owner_id: Optional[float]
    is_sold: Optional[bool] = False
    end_date: Optional[datetime]


class AuctionUserCreate(BaseModel):
    """Create user from API data and save it to database"""

    username: str


class AuctionUserRead(BaseModel):
    """Read user from database"""

    id: int
    username: str
    items: list[AuctionItemRead] = []

    class Config:
        orm_mode = True
