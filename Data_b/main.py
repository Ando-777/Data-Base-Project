from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Festival(Base):
    __tablename__ = 'festivals'


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel

class FestivalBase(BaseModel):
    name: str
    location: str
    date: str  
    organizer: str
    format: str

class FestivalCreate(FestivalBase):
    pass

class Festival(FestivalBase):
    id: int

    class Config:
        orm_mode = True

@app.post("/festivals/", response_model=Festival)
def create_festival(festival: FestivalCreate, db: Session = Depends(get_db)):
    db_festival = Festival(**festival.dict())
    db.add(db_festival)
    db.commit()
    db.refresh(db_festival)
    return db_festival

@app.get("/festivals/", response_model=List[Festival])
def read_festivals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    festivals = db.query(Festival).offset(skip).limit(limit).all()
    return festivals

@app.get("/festivals/{festival_id}", response_model=Festival)
def read_festival(festival_id: int, db: Session = Depends(get_db)):
    db_festival = db.query(Festival).filter(Festival.id == festival_id).first()
    if db_festival is None:
        raise HTTPException(status_code=404, detail="Festival not found")
    return db_festival

@app.put("/festivals/{festival_id}", response_model=Festival)
def update_festival(festival_id: int, festival: FestivalCreate, db: Session = Depends(get_db)):
    db_festival = db.query(Festival).filter(Festival.id == festival_id).first()
    if db_festival is None:
        raise HTTPException(status_code=404, detail="Festival not found")
    for var, value in vars(festival).items():
        setattr(db_festival, var, value) if value else None
    db.commit()
    db.refresh(db_festival)
    return db_festival

@app.delete("/festivals/{festival_id}", status_code=204)
def delete_festival(festival_id: int, db: Session = Depends(get_db)):
    db_festival = db.query(Festival).filter(Festival.id == festival_id).first()
    if db_festival is None:
        raise HTTPException(status_code=404, detail="Festival not found")
    db.delete(db_festival)
    db.commit()
    return {"ok": True}
