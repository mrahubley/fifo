from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix='/profiles',tags=['Profiles'])


@router.get('/', response_model=List[schemas.GetProfile])
def get_profiles(db: Session = Depends(get_db)):
    query = db.query(models.Profile).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile found")
    return query



@router.get('/{id}', response_model=schemas.GetProfile)
def get_profile(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Profile id {id} not found")
    return query



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GetProfile)
def create_profile(profile: schemas.CreateProfile, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Profile).filter(models.Profile.account_id == user_id.id)
    check_email = query.first()
    if not check_email:
      
        profile = models.Profile(account_id=user_id.id,**profile.dict())
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= f"Email {profile.email} already exist")



@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.GetProfile)
def update_profile(id: int, profile: schemas.UpdateProfile, db: Session = Depends(get_db)):
    query = db.query(models.Profile).filter(models.Profile.id == id)
    check_query = query.first()
    if not check_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Profile id {id} not found")
    query.update(profile.dict(), synchronize_session=False)
    db.commit()
    db.refresh(profile)
    return profile



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(id: int , db: Session = Depends(get_db)):
    query = db.query(models.Profile).filter(models.Profile.id == id)
    check_query = query.first()
    if not check_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Profile with id {id} not found")
    query.delete(synchronize_session=False)
    db.commit()