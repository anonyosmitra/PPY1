from sqlalchemy import Column, Integer, String,TIMESTAMP,Boolean,ForeignKey
from sqlalchemy.orm import relationship, declarative_base, mapped_column

Base = declarative_base()
class userSession(Base):
    __tablename__="session"
    id=mapped_column(Integer,primary_key=True)
    userId=mapped_column(String,ForeignKey("user.id"))
    active=mapped_column(Boolean)
    login=mapped_column(TIMESTAMP)
    logout=mapped_column(TIMESTAMP,nullable=True)
    user = relationship("users",foreign_keys=[userId])
class user(Base):
    __tablename__="users"
    id=mapped_column(Integer,primary_key=True)
    name=mapped_column(String,unique=True)
    password=mapped_column(String)
    sessions = relationship("session")
class test(Base):
    __tablename__="test"
    a=mapped_column(String,primary_key=True)
    b=mapped_column(Integer)