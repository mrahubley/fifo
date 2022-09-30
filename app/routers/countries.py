from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix='/countries', tags=['Countries'])

#Get accounts
@router.get('/', response_model=List[schemas.Country])
def get_countries(db: Session = Depends(get_db)):
    query = db.query(models.Country).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No country found!")
    return query



@router.get('/{id}', response_model=schemas.Country)
def get_country(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Country).filter(models.Country.id == id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Country id {id} not found")
    return query



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Country)
def create_country(country: schemas.CreateCountry, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Country).filter(models.Country.name == country.name)
    check_query = query.first()
    if not check_query:
        country = models.Country(account_id=user_id.id, **country.dict())
        db.add(country)
        db.commit()
        db.refresh(country)       
        return country
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Country already exist")
        


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Country)
def update_country(id: int, country: schemas.CreateCountry, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Country).filter(models.Country.id == id)
    check_query = query.first()
    if not check_query:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country id {id} not found")
    query.update(country.dict(), synchronize_session=False)
    db.commit()
    return check_query



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_country(id: int , db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Country).filter(models.Country.id == id)
    del_query = query.first()
    if not del_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account id {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    