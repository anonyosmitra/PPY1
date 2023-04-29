from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, joinedload
import socket
from models import Base
endpoint = "dbserver.anonyo.net"
endpoint = socket.gethostbyname(endpoint)
user = "s25833"
port = 3306
passwd = "test"
dbName="PJWSTK"
class Connect:
    def __init__(self):
        try:
            self.cnx=create_engine(f'mysql+pymysql://{user}:{passwd}@{endpoint}/{dbName}')
            self.cur=self.cnx.connect()
            self.ses = sessionmaker(bind=self.cnx)
            Base.metadata.create_all(self.cnx)
        except Exception as e:
            print(e.with_traceback())
    def test(self,query:str):
        result = self.cur.execute(text(query))
        for row in result:
            print(row)
    def add(self,obj):
        s=self.ses()
        s.add(obj)
        s.commit()
        s.close()
    def join(self,tabs):
        s = self.ses()
        a=s.query(tabs[0])
        for i in tabs[1:]:
            a=a.join(i)
            a=a.options(joinedload(tabs[0].i))
        a=a.all()
        s.close()
        return a
    def select(self,Cls,where=None,orderBy=None,limit=None):#fix where filter
        s = self.ses()
        a= s.query(Cls)
        if where is not None:
            a=a.filter(where)
        if orderBy is not None:
            a=a.order_by(orderBy)
        if limit is None:
            a=a.all()
        else:
            a=a.limit(limit)
        s.close()
        return a
    def close(self):
        self.cnx.dispose()