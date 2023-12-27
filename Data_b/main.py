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
    pass

@app.get("/festivals/", response_model=List[Festival])
def read_festivals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pass

@app.get("/festivals/{festival_id}", response_model=Festival)
def read_festival(festival_id: int, db: Session = Depends(get_db)):
    pass

@app.put("/festivals/{festival_id}", response_model=Festival)
def update_festival(festival_id: int, festival: FestivalCreate, db: Session = Depends(get_db)):
    pass

@app.delete("/festivals/{festival_id}")
def delete_festival(festival_id: int, db: Session = Depends(get_db)):
    pass
