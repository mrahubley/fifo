from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix='/degrees', tags=['Degrees'])



@router.get('/', response_model=List[schemas.Degree])
def get_degrees(db: Session = Depends(get_db)):
    query = db.query(models.Degree).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No degree found!")
    return query



@router.get('/{id}', response_model=schemas.Degree)
def get_degree(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Degree).filter(models.Degree.id == id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Degree id {id} not found")
    return query



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Degree)
def create_degree(degree: schemas.CreateDegree, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Degree).filter(models.Degree.name == degree.name)
    check_query = query.first()
    if not check_query:
        degree = models.Degree(**degree.dict())
        db.add(degree)
        db.commit()
        db.refresh(degree)       
        return degree
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Degree already exist")
        


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Degree)
def update_degree(id: int, degree: schemas.CreateDegree, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Degree).filter(models.Degree.id == id)
    check_query = query.first()
    if not check_query:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Degree id {id} not found")
    query.update(degree.dict(), synchronize_session=False)
    db.commit()
    return check_query



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_degree(id: int , db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Degree).filter(models.Degree.id == id)
    del_query = query.first()
    if not del_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Degree id {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    