from typing import Union

from sqlalchemy import create_engine, text, ClauseElement
from sqlalchemy.orm import sessionmaker, joinedload
import socket
from models.models import ORMBase,User
endpoint = "dbserver.anonyo.net"
endpoint = socket.gethostbyname(endpoint)
user = "s25833"
port = 3306
passwd = "test"
dbName="PJWSTK"
def to_dict(obj):
    result = {}
    for key, value in obj.__dict__.items():
        if key.startswith('_'):
            continue
        if isinstance(value, (list, tuple)):
            result[key] = [to_dict(item) if isinstance(item, ORMBase) else item for item in value]
        elif isinstance(value, ORMBase):
            result[key] = to_dict(value)
        else:
            result[key] = value
    return result
def add(obj,returnObj=False):
    con=Connect()
    i=con.add(obj,returnObj)
    con.close()
    return i
class Connect:
    def __init__(self):
        try:
            self.cnx=create_engine(f'mysql+pymysql://{user}:{passwd}@{endpoint}/{dbName}')
            self.cur=self.cnx.connect()
            self.sesMake = sessionmaker(bind=self.cnx)
            self.ses=self.sesMake()
            ORMBase.metadata.create_all(self.cnx)
        except Exception as e:
            print(e.with_traceback())
    def getSes(self):
        if not self.ses:
            self.ses=self.sesMake()
        return self.ses
    def killSes(self):
        if not self.ses:
            self.ses.close()
    def test(self,query:str):
        result = self.cur.execute(text(query))
        for row in result:
            print(row)
    def add(self,obj,returnObj=False):
        s=self.getSes()
        s.add(obj)
        s.commit()
        id=None
        if returnObj:
            return obj
    def delete(self,obj):
        s = self.getSes()
        s.delete(obj)
        s.commit()
    def commit(self):
        s=self.getSes()
        s.commit()
    def join(self,tabs):
        s = self.getSes()
        a=s.query(tabs[0])
        for i in tabs[1:]:
            a=a.join(i)
            a=a.options(joinedload(tabs[0].i))
        a=a.all()
        return a

    def select(self,Cls,where: Union[ClauseElement, bool],orderBy=None,limit=None):#fix where filter
        s = self.getSes()
        a= s.query(Cls)
        if where is not None:
            a=a.filter(where)
        if orderBy is not None:
            a=a.order_by(orderBy)
        if limit is not None:
            a=a.limit(limit)
        a = a.all()
        return a
    def close(self):
        self.killSes()
        self.cnx.dispose()