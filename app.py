from typing import Union
from fastapi import FastAPI,requests,Request,Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import dbHandler as dbh
import accounts as acc
import timezone as tz
import datetime as dt
#Set sys timezone to UTC before running
from pydantic import BaseModel
import uvicorn,time
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    session = request.cookies.get("session")
    userid=acc.getUser(session)
    if userid:
        username = dbh.select("users", ["name"], {"id": userid})
        if len(username)==0:
            return templates.TemplateResponse("login.html", {"request": request})
        username=username[0]["name"]
        print("returning user: "+username)
        return templates.TemplateResponse("homePage.html", {"request": request, "username": username,"session":session})
    return templates.TemplateResponse("login.html", {"request": request,"msg":""})
@app.post("/")
async def login(request: Request):
    frm=await request.form()
    con=dbh.Connect()
    user=con.select("users",["id","name","password"],{"name":frm["username"]})
    if len(user)==0:
        con.close()
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid username or password"})
    else:
        user=user[0]
        if acc.checkPassword(user["password"],frm["password"]):
            session=con.insert("session",{"userId":user["id"],"active":True,"login":dt.datetime.now()},returnid=id)
            con.close()
            return templates.TemplateResponse("homePage.html",{"request": request, "username": frm["username"], "session": session})
        else:

            con.close()
            return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid username or password"})

@app.post("/signup")
async def signup(request: Request):
    con=dbh.Connect()
    frm = await request.form()
    if len(con.select("users",["id"],{"name":frm["username"]}))==1:
        con.close()
        return templates.TemplateResponse("signup.html", {"request": request, "msg": "Username already exists"})
    if frm["password1"]!=frm["password2"]:
        con.close()
        return templates.TemplateResponse("signup.html", {"request": request, "msg": "Passwords don't match"})
    hs=acc.genPass(frm["password1"])
    userId=con.insert("users",{"name":frm["username"],"password":hs},returnid=True)
    session=con.insert("session",{"userId":userId,"active":True,"login":dt.datetime.now()},returnid=id)
    con.close()
    return HTMLResponse(content='<script>document.cookie="session={}";window.location="/";</script>'.format(session))

@app.get("/signup")
def signupForm(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "msg": ""})
@app.get("/logout")
def logout(request: Request):
    session = request.cookies.get("session")
    dbh.update("session",{"active":False,"logout":dt.datetime.now()},{"id":session})
    return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')

if __name__ == "__main__":
    if time.timezone == 0 or time.timezone==3600:
        uvicorn.run(app, host="localhost", port=5800)
    else:
        print("Please change system timezone to UTC")