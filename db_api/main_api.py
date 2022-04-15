from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn

import crud, models, schemas
from database import SessionLocal, engine
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(e)
    print('pepe')
    raise e
    


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# read more in figma file
# https://www.figma.com/file/7Rmtk9aiGvOyfKEPJMqfxG/bot-alg?node-id=69%3A1826

# create item
@app.post("/auc_ext/create_item/", response_model=schemas.AuctionItemRead)
def create_item(item: schemas.AuctionItemCreate, db: Session = Depends(get_db)):
    return crud.auc_item_create(db=db, item=item, )

# read item by id
@app.get("/auc_ext/item_by_id/", response_model=schemas.AuctionItemRead)
def read_item_by_id(id: int, db: Session = Depends(get_db)):
    return crud.auc_item_read_by_id(db, id=id)

# read all items
@app.get("/auc_ext/items/", response_model=list[schemas.AuctionItemRead])
def read_all_items(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud.auc_item_read(db, skip=skip, limit=limit)

# update item by id
@app.put("/auc_ext/update_item_by_id/", response_model=schemas.AuctionItemRead)
def update_item_by_id(
    item: schemas.AuctionItemUpdateReq, 
    item_id: int, 
    price_increment: float = None,
    db: Session = Depends(get_db)
):
    return crud.update_item_by_id(
        db=db, 
        item=item, 
        item_id=item_id, 
        price_increment=price_increment,
    )

# update item by title
@app.put("/auc_ext/update_item_by_title/", response_model=schemas.AuctionItemRead)
def update_item_by_title(
    item: schemas.AuctionItemUpdateReq, 
    # item_id:int, 
    price_increment: float = None,
    db: Session = Depends(get_db)
):
    return crud.update_item_by_title(
        db=db, 
        item=item, 
        price_increment=price_increment,
    )

# delete item by id
@app.delete("/auc_ext/delete_item_by_id/", response_model=bool)
def delete_item_by_id(id: int, db: Session = Depends(get_db))-> bool:
    return crud.auc_item_delete_by_id(
        db=db,
        item_id=id,
    )

# delete item by title
@app.delete("/auc_ext/delete_item_by_title/", response_model=bool)
def delete_item_by_title(title: int, db: Session = Depends(get_db))-> bool:
    return crud.auc_item_delete_by_title(
        db=db,
        item_title=title,
    )


# create user
@app.post("/auc_ext/create_user/", response_model=schemas.AuctionUserRead)
def create_user(user: schemas.AuctionUserCreate, db: Session = Depends(get_db)):
    return crud.auc_user_create(db=db, user=user, )


# read user by id
@app.get("/auc_ext/user_by_id/", response_model=schemas.AuctionUserRead)
def read_user_by_id(id: int, db: Session = Depends(get_db)):
    return crud.auc_user_read_by_id(db, id=id)

# read user by username
@app.get("/auc_ext/user_by_username/", response_model=schemas.AuctionUserRead)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    return crud.auc_user_read_by_username(db, username=username)

# read all users
@app.get("/auc_ext/users/", response_model=list[schemas.AuctionUserRead])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.auc_user_read_all(db, skip=skip, limit=limit)

# update user by id
@app.put("/auc_ext/update_user_by_id/", response_model=schemas.AuctionUserRead)
def update_user_by_id(
    id: int,
    username: str, 
    db: Session = Depends(get_db)
):
    return crud.auc_user_update(db=db, id=id, username=username, )

# delete user by id
@app.delete("/auc_ext/delete_user_by_id/", response_model=bool)
def delete_user_by_id(id: int, db: Session = Depends(get_db))-> bool:
    return crud.auc_user_delete_by_id(
        db=db,
        id=id,
    )
# delete user by username
@app.delete("/auc_ext/delete_user_by_username/", response_model=bool)
def delete_user_by_username(username: int, db: Session = Depends(get_db))-> bool:
    return crud.auc_user_delete_by_username(
        db=db,
        username=username,
    )




if __name__ == '__main__':
    import os
    PORT=os.getenv('PORT', 8001)
    
    uvicorn.run(app, debug=1, host="0.0.0.0", port=PORT)