# from datetime import datetime
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression

from src.api.database import Base


class AuctionItem(Base):
    __tablename__ = "auction_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    price = Column(
        Integer,
    )
    is_start_price = Column(
        Boolean,
    )
    photo = Column(
        String,
    )  # new table w/ links to pictures list[str|str...]
    owner_id = Column(Integer, ForeignKey("auction_users.id"))
    is_sold = Column(Boolean, default=False)
    start_date = Column(
        DateTime,
    )
    end_date = Column(
        DateTime,
    )

    owner = relationship("AuctionUser", back_populates="items")  # ???


class AuctionUser(Base):
    __tablename__ = "auction_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    items = relationship("AuctionItem", back_populates="owner")  # ???


class AuctionItemUpdate(BaseModel):
    """Update item in database from API data"""

    title: Optional[Union[str, InstrumentedAttribute]]
    description: Optional[Union[str, InstrumentedAttribute]]
    price: Optional[Union[float, InstrumentedAttribute, BinaryExpression]]
    is_start_price: Optional[Union[bool, InstrumentedAttribute]] = False
    owner_id: Optional[Union[float, InstrumentedAttribute]]
    is_sold: Optional[Union[bool, InstrumentedAttribute]] = False
    end_date: Optional[Union[datetime, InstrumentedAttribute]]

    class Config:
        require_by_default = False  # use Required[]
        arbitrary_types_allowed = True
        orm_mode = True
