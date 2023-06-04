from fastapi import FastAPI, HTTPException
from models.models import CredDTO,User,UserSession,CurrentWeather,HourlyLoc,Coordinates,MapResp,Settings
import uvicorn
import accounts as acc
import dbHandler2 as dbh
import timezone as tz
import weather
import location
from typing import Dict, Any
app=FastAPI()

@app.post("/currentWeather")
def curWeather(req: Dict[str, Any]):
    con=dbh.Connect()
    user=acc.getUser(req["session"],con)
    if user is None:
        con.close()
        raise HTTPException(400, detail="Invalid Session")
    resp=CurrentWeather(session=req["session"],username=user.name,tempUnit="C",locs=weather.getCurrentWeather(user,con))
    if user.imperial:
        resp.tempUnit="F"
    con.close()
    return resp.dict()
@app.post("/hourly")
def hourly(req: Dict[str, Any]):
    con = dbh.Connect()
    user = acc.getUser(req["session"], con)
    if user is None:
        con.close()
        raise HTTPException(400, detail="Invalid Session")
    loc=location.getCoordinates(req["location"],user,con)
    if loc is None:
        con.close()
        raise HTTPException(404, detail="Unknown Location")
    zone=location.getInfo(req["ip"])
    we=weather.getHourlyWeather(user,loc,con,zone["timezone"])
    resp=HourlyLoc(username=user.name,session=req["session"],tempUnit="C",location=loc.name,locationId=loc.id,weathers=we)
    if user.imperial:
        resp.tempUnit="F"
    con.close()
    return resp
@app.post("/login")
def login(cred: CredDTO):
    con=dbh.Connect()
    a=list(con.select(User,User.name==cred.username,limit=1))
    if len(a)==0 or not acc.checkPassword(a[0].password,cred.password):
        con.close()
        raise HTTPException(400,detail="Invalid username or password")
    ses=acc.makeSession(a[0],con)
    ret= {"userId":a[0].id,"username":a[0].name,"session":ses.id}
    con.close()
    return ret
@app.post("/signup")
def signup(cred:CredDTO):
    con=dbh.Connect()
    a = list(con.select(User, User.name == cred.username, limit=1))
    if len(a) == 1:
        con.close()
        raise HTTPException(400, detail="Username already exists")
    pw=acc.genPass(cred.password)
    a=User(name=cred.username,password=pw)
    con.add(a,returnObj=True)
    l=location.getInfo(cred.ip)
    l=Coordinates(userId=a.id,lat=l["lat"],lon=l["lon"],name=l["city"])
    con.add(l)
    ses = acc.makeSession(a,con)
    ret = {"userId": a.id, "username": a.name, "session": ses.id}
    con.close()
    return ret
@app.post("/logout")
def logout(req: Dict[str, Any]):
    con=dbh.Connect()
    resp = {"userId": None, "username": None, "session": req["session"]}
    a = list(con.select(UserSession, UserSession.id == req["session"], limit=1))
    if len(a)==1:
        a=a[0]
        a.logout=tz.timeIn("UTC",fmt=None)
        con.commit()
    con.close()
    return HTTPException(200)
@app.post("/settings")
async def settings(req: Dict[str, Any]):
    con = dbh.Connect()
    user = acc.getUser(req["session"], con)
    if user is None:
        con.close()
        raise HTTPException(400, detail="Invalid Session")
    if "unit" in req:
        user.imperial=req["unit"]=="imperial"
        con.commit()
    if "loc" in req:
        loc=location.getCoordinates(int(req["loc"]),user,con)
        if loc is not None:
            con.delete(loc)
    resp=Settings(username=user.name,unit="metric",locs=location.getLocations(user,con))
    if user.imperial:
        resp.unit="imperial"
    con.close()
    return resp

@app.post("/map")
def map(loc:Dict[str, Any]):
    con=dbh.Connect()
    user=acc.getUser(loc["session"],con)
    if user is None:
        con.close()
        raise HTTPException(400, detail="Invalid Session")
    if "ip" in loc:
        info=location.getInfo(loc["ip"])
        loc["lat"]=info["lat"]
        loc["lon"]=info["lon"]
    if "name" in loc:
        cord=Coordinates(userId=user.id,lat=loc["lat"],lon=loc["lon"],name=loc["name"])
        con.add(cord)
        con.close()
        raise HTTPException(202, detail="Redirect")
    wet=weather.getWeather(loc,user,con)
    resp=MapResp(username=user.name,lat=loc["lat"],lon=loc["lon"],temp=wet.temp,weather=wet.weather,tempUnit="C")
    if user.imperial:
        resp.tempUnit="F"
    con.close()
    return resp
def run():
    if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=5001)

