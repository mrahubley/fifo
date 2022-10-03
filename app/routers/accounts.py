from ast import parse
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from ..utils import hashpassword
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import or_

router = APIRouter(prefix='/accounts', tags=['Accounts'])


#Get accounts
@router.get('/', response_model=List[schemas.Accounts])
def get_accounts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    query = db.query(models.Account).filter(models.Account.email.contains(search)).limit(limit).offset(skip).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No account found!")
    return query



@router.get('/{id}', response_model=schemas.Accounts)
def get_account(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Account).filter(models.Account.id == id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Account id {id} not found")
    return query



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Accounts)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    query = db.query(models.Account).filter(or_(models.Account.email == account.email, models.Account.number == account.number))
    check_query = query.first()
    pwd_hashed = hashpassword(account.password)
    if not check_query:
        account.password = pwd_hashed
        account = models.Account(**account.dict())
        db.add(account)
        db.commit()
        db.refresh(account)       
        return account
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= f"Account already exist")
        


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Accounts)
def update_account(id: int, account: schemas.AccountUpdate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Account).filter(models.Account.id == id)
    check_query = query.first()
    if not check_query:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Account id {id} not found")
    if account.email == None:
        account.email = check_query.email
    if account.number == None:
        account.number ==  check_query.number
    print(account.number)
    query.update(account.dict(), synchronize_session=False)
    db.commit()
    return check_query



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_account(id: int , db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Account).filter(models.Account.id == id)
    del_query = query.first()
    if not del_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Account id {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    