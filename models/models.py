from typing import List

from sqlalchemy import Column, Integer, String,TIMESTAMP,Boolean,ForeignKey,Float
from sqlalchemy.orm import relationship, declarative_base, mapped_column
from pydantic import BaseModel as DTOBase

ORMBase = declarative_base()
class CredDTO(DTOBase):
    username: str
    password: str
    ip:str
class MapResp(DTOBase):
    username:str
    lat: float
    lon: float
    temp: float
    weather: str
    tempUnit: str
class Location(DTOBase):
    id: int
    name: str
class Settings(DTOBase):
    username:str
    unit: str
    locs:List[Location]

class Weather(DTOBase):
    temp: float
    weather: str
class WeatherAtIp(DTOBase):
    session: int
    ip: str
class GetWeatherIn(DTOBase):
    session: int
    lat: float
    lon: float

class AddNewLocation(DTOBase):
    session: int
    name: str
    lat: float
    lon: float
class CurrentWeatherLoc(DTOBase):
    id: int
    name: str
    temp: float
    weather: str
class HourlyWeather(DTOBase):
    time: str
    temp: float
    weather: str
class HourlyLoc(DTOBase):
    username: str
    session: int
    tempUnit: str
    location: str
    locationId: int
    weathers:List[HourlyWeather]
class CurrentWeather(DTOBase):
    username: str
    session: int
    tempUnit: str
    locs: List[CurrentWeatherLoc]
class UserSession(ORMBase):
    __tablename__='session'
    id=Column(Integer,primary_key=True)
    userId=Column(Integer,ForeignKey('user.id'))
    login=Column(TIMESTAMP)
    logout=Column(TIMESTAMP,nullable=True,default=None)
    user = relationship('User', backref='sessions')
class User(ORMBase):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    name=Column(String,unique=True)
    password=Column(String)
    imperial=Column(Boolean,default=False)
class Coordinates(ORMBase):
    __tablename__='coordinates'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    lat=Column(Float)
    lon=Column(Float)
    name=Column(String)
    user = relationship('User', backref='coordinates')
"""class test(ORMBase):
    __tablename__="test"
    a=mapped_column(String,primary_key=True)
    b=mapped_column(Integer)"""