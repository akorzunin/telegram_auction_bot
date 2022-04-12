# from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

try:
    from database import Base
except ModuleNotFoundError:
    from db_api.database import Base # TODO fix it


class AuctionItem(Base):
    __tablename__ = "auction_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    price = Column(Integer, )
    is_start_price = Column(Boolean, )
    photo = Column(String, ) # new table w/ links to pictures list[str|str...]
    owner_id = Column(Integer, ForeignKey("auction_users.id"))
    is_sold = Column(Boolean, default=False)
    start_date = Column(DateTime, )
    end_date = Column(DateTime, )

    owner = relationship("AuctionUser", back_populates="items") #???

class AuctionUser(Base):
    __tablename__ = "auction_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    items = relationship("AuctionItem", back_populates="owner") #???