from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix= '/jobs',
    tags=['Jobs']
)

#Get all jobs
@router.get('/', response_model=List[schemas.Jobs])
def get_jobs(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: Optional[int]=10, skip: Optional[int]=0, search: Optional[str]=""):
    job_query = db.query(models.Job).filter(or_(models.Job.name.contains(search), models.Job.description.contains(search))).limit(limit).offset(skip).all()
    if not job_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No job found!")
    return job_query



#Get a job by ID
@router.get('/{id}', response_model=schemas.Jobs)
def get_job(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Job).filter(models.Job.id == id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job id {id} not found.")
    return query



#Add new job
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Jobs)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    job.account_id = user_id.id
    job = models.Job(**job.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


#Update a job by ID
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Jobs)
def update_job(id: int, job: schemas.JobCreate, db: Session = Depends(get_db)):
    query = db.query(models.Job).filter(models.Job.id == id)
    check_query = query.first()
    if not check_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Job id {id} does not exist")
    query.update(job.dict(), synchronize_session=False)
    db.commit()
    return check_query


#Delete a job by ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_job(id: int , db: Session = Depends(get_db)):
    job_query = db.query(models.Job).filter(models.Job.id == id).first()
    if job_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Job id {id} does not exist")
    db.query(models.Job).filter(models.Job.id == id).delete(synchronize_session=False)
    db.commit()
    