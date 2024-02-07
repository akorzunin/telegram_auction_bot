from sqlalchemy.orm import Session

from src.api import models, schemas

# read more in figma file
# https://www.figma.com/file/7Rmtk9aiGvOyfKEPJMqfxG/bot-alg?node-id=69%3A1826


# create item
def auc_item_create(db: Session, item: schemas.AuctionItemCreate):
    db_item = models.AuctionItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# read item by id
def auc_item_read_by_id(db: Session, id: int):
    return db.query(models.AuctionItem).get(id)


# read all items
def auc_item_read(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AuctionItem).offset(skip).limit(limit).all()


# update item by id
def update_item_by_id(
    db: Session,
    item: models.AuctionItemUpdate,
    item_id: int,
    price_increment: float = None,
):

    # remove all None values from recived item
    upd_dict = {k: v for k, v in item.dict().items() if v is not None}
    defalut_dict = dict(
        title=models.AuctionItem.title,
        description=models.AuctionItem.description,
        price=(
            models.AuctionItem.price
            if price_increment is None
            else models.AuctionItem.price + price_increment
        ),
        is_start_price=models.AuctionItem.is_start_price,
        owner_id=models.AuctionItem.owner_id,
        is_sold=models.AuctionItem.is_sold,
        end_date=models.AuctionItem.end_date,
    )
    _ = (
        db.query(models.AuctionItem)
        .filter_by(id=item_id)
        .update(
            # validate data
            schemas.AuctionItemUpdate(
                **dict(
                    # merge 2 dicts w/ default data and updated data
                    defalut_dict,
                    **upd_dict
                )
            ).model_dump()
        )
    )
    db.commit()

    return db.query(models.AuctionItem).get(item_id)


# update item by title
def update_item_by_title(
    db: Session, item: models.AuctionItemUpdate, price_increment: float = None
):

    # remove all None values from recived item
    upd_dict = {k: v for k, v in item.dict().items() if v is not None}
    defalut_dict = dict(
        title=models.AuctionItem.title,
        description=models.AuctionItem.description,
        price=(
            models.AuctionItem.price
            if price_increment is None
            else models.AuctionItem.price + price_increment
        ),
        is_start_price=models.AuctionItem.is_start_price,
        owner_id=models.AuctionItem.owner_id,
        is_sold=models.AuctionItem.is_sold,
        end_date=models.AuctionItem.end_date,
    )
    db_item = (
        db.query(models.AuctionItem)
        .filter_by(title=item.title)
        .update(
            # validate data
            models.AuctionItemUpdate(
                **dict(
                    # merge 2 dicts w/ default data and updated data
                    defalut_dict,
                    **upd_dict
                )
            ).dict()
        )
    )

    db.commit()
    return db_item


# delete item by id
def auc_item_delete_by_id(db: Session, item_id: int) -> bool:
    db_item = db.query(models.AuctionItem).filter_by(id=item_id).delete()
    db.commit()
    return db_item  # true or false


# delete item by title
def auc_item_delete_by_title(db: Session, item_title: str) -> bool:
    db_item = db.query(models.AuctionItem).filter_by(title=item_title).delete()
    db.commit()
    return db_item  # true or false


# create user
def auc_user_create(db: Session, user: schemas.AuctionUserCreate):
    db_user = models.AuctionUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# read user by id
def auc_user_read_by_id(db: Session, id: int):
    return db.query(models.AuctionUser).get(id)


# read user by username
def auc_user_read_by_username(db: Session, username: str):
    return db.query(models.AuctionUser).filter_by(username=username).first()


# read all users
def auc_user_read_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AuctionUser).offset(skip).limit(limit).all()


# update user by id
def auc_user_update(db: Session, id: int, username: str):
    _ = db.query(models.AuctionUser).filter_by(id=id).update(dict(username=username))
    db.commit()
    return db.query(models.AuctionUser).get(id)


# delete user by id
def auc_user_delete_by_id(db: Session, id: int):
    db_item = db.query(models.AuctionUser).filter_by(id=id).delete()
    db.commit()
    return db_item


# delete user by username
def auc_user_delete_by_username(db: Session, username: str):
    db_item = db.query(models.AuctionUser).filter_by(username=username).delete()
    db.commit()
    return db_item
