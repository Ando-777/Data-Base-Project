from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

performance_rockgroup_table = Table('performance_rockgroup', Base.metadata,
    Column('performance_id', ForeignKey('performances.id'), primary_key=True),
    Column('rockgroup_id', ForeignKey('rockgroups.id'), primary_key=True)
)

class Festival(Base):
    __tablename__ = 'festivals'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    location = Column(String(255))
    date = Column(Date)
    organizer = Column(String(255))
    format = Column(String(255))  
    performances = relationship("Performance", back_populates="festival")

class Performance(Base):
    __tablename__ = 'performances'

    id = Column(Integer, primary_key=True)
    type = Column(String(255))  
    number = Column(Integer) 
    duration = Column(Integer)  

    festival_id = Column(Integer, ForeignKey('festivals.id'))

    festival = relationship("Festival", back_populates="performances")
    rockgroups = relationship("RockGroup",
                              secondary=performance_rockgroup_table,
                              back_populates="performances")

class RockGroup(Base):
    __tablename__ = 'rockgroups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    year_formed = Column(Date)
    genre = Column(String(255))  
    members = Column(String(255))  
    performances = relationship("Performance",
                                secondary=performance_rockgroup_table,
                                back_populates="rockgroups")

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
