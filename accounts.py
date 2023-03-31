import bcrypt
import dbHandler as dbh
def genPass(ps:str):
    password = ps.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password
def checkPassword(hs,pw):
    pw=pw.encode('utf-8')
    return bcrypt.checkpw(pw,hs.encode('utf-8'))
def getUser(session,con=None):
    killCon=False
    if not con:
        con=dbh.Connect()
        killCon=True
    a=con.select("session",["userId"],{"id":session,"active":True})
    if killCon:
        con.close()
    if a:
        return a[0]["userId"]
    else:
        return None
