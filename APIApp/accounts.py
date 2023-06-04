import bcrypt
from models.models import User,UserSession
import timezone as tz
import dbHandler2 as dbh
def genPass(ps:str)->str:
    password = ps.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password
def getUser(ses:int,con:dbh.Connect)->User:
    a = list(con.select(UserSession, UserSession.id == ses, limit=1))
    if len(a) == 0 or a[0].logout is not None:
        return None
    else:
        return a[0].user

def checkPassword(hs:str,pw:str)->str:
    pw=pw.encode('utf-8')
    return bcrypt.checkpw(pw,hs.encode('utf-8'))
def makeSession(user:User,con:dbh.Connect)-> UserSession:
    ses=UserSession(userId=user.id,login=tz.timeIn("UTC",fmt=None))
    sesId=con.add(ses,returnObj=True)
    return sesId
