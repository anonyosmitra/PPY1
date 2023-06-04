from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests as HTTPRequests
from fastapi.responses import HTMLResponse,RedirectResponse
import json,uvicorn
from models.models import CredDTO,WeatherAtIp,GetWeatherIn,AddNewLocation

api="http://localhost:5001/"

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
headers = {'Content-Type': 'application/json'}

@app.get("/")
def home(request: Request):
    session = request.cookies.get("session")
    if session is not None:
        resp=HTTPRequests.post(api+"currentWeather",data=json.dumps({"session":session}))
        if resp.status_code!=200:
            return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')
        resp=json.loads(resp.text)
        r={"request": request}
        r.update(resp)
        return templates.TemplateResponse("homePage.html",r)
    return templates.TemplateResponse("login.html", {"request": request, "msg": ""})

@app.post("/settings")
async def updateSettings(request:Request):
    session = request.cookies.get("session")
    if session is None:
        return RedirectResponse(url="/")
    frm = await request.form()
    frm=dict(frm)
    frm.update({"session":session})
    resp = HTTPRequests.post(api + "settings", data=json.dumps(frm))
    if resp.status_code != 200:
        return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')
    r = {"request": request}
    r.update(json.loads(resp.text))
    return templates.TemplateResponse("SettingsPage.html", r)

@app.get("/settings")
async def settings(request:Request):
    session = request.cookies.get("session")
    if session is None:
        return RedirectResponse(url="/")
    resp = HTTPRequests.post(api + "settings", data=json.dumps({"session": session}))
    if resp.status_code != 200:
        return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')
    r = {"request": request}
    r.update(json.loads(resp.text))
    return templates.TemplateResponse("SettingsPage.html", r)
@app.get("/map")
async def map(request: Request):
    session = request.cookies.get("session")
    if session is None:
        return RedirectResponse(url="/")
    req=WeatherAtIp(session=session,ip=request.client.host)
    resp = HTTPRequests.post(api + "map", data=req.json())
    if resp.status_code==400:
        return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')
    r={"request": request}
    r.update(json.loads(resp.text))
    return templates.TemplateResponse("mapPage.html", r)

@app.post("/map")
async def mapRoute(request:Request):
    session = request.cookies.get("session")
    if session is None:
        return RedirectResponse(url="/")
    frm = await request.form()
    req=None
    if "name" in frm:
        req=AddNewLocation(session=session,name=frm["name"],lat=frm["lat"],lon=frm["lon"])
    else:
        req=GetWeatherIn(session=session,lat=frm["lat"],lon=frm["lon"])
    resp = HTTPRequests.post(api + "map", data=req.json())
    if resp.status_code==400:
        return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')
    if resp.status_code==202:
        return HTMLResponse(content='<script>window.location="/";</script>')
    r = {"request": request}
    r.update(json.loads(resp.text))
    return templates.TemplateResponse("mapPage.html", r)
@app.post("/")
async def login(request: Request):
    frm = await request.form()
    cred=CredDTO(username=frm["username"],password=frm["password"],ip=request.client.host)
    resp=HTTPRequests.post(api+"login",cred.json())
    if resp.status_code!=200:
        return templates.TemplateResponse("login.html", {"request": request, "msg": json.loads(resp.text)["detail"]})
    resp=json.loads(resp.text)
    return HTMLResponse(content='<script>document.cookie="session= {}";location.href="/";</script>'.format(resp["session"]))
@app.get("/signup")
def signupForm(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "msg": "","username":""})

@app.get("/hourly/{id}")
async def hourly(id:int,request: Request):
    session = request.cookies.get("session")
    if session is None:
        return RedirectResponse(url="/")
    resp = HTTPRequests.post(api + "hourly", data=json.dumps({"session": session,"location":id,"ip":request.client.host}))
    if resp.status_code==400:
        return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')
    if resp.status_code==404:
        return templates.TemplateResponse("layout.html",{"request": request,"info":json.loads(resp.text)["detail"]})
    resp = json.loads(resp.text)
    r = {"request": request}
    r.update(resp)
    return templates.TemplateResponse("hourlyPage.html", r)
@app.post("/signup")
async def signup(request: Request):
    frm= await request.form()
    if frm["password1"]!=frm["password2"]:
        return templates.TemplateResponse("signup.html", {"request": request, "msg": "Passwords don't match","username":frm["username"]})
    cred=CredDTO(username=frm["username"],password=frm["password1"],ip=request.client.host)
    resp=HTTPRequests.post(api+"signup",cred.json())
    if resp.status_code!=200:
        return templates.TemplateResponse("signup.html", {"request": request, "msg": json.loads(resp.text)["detail"]})
    resp = json.loads(resp.text)
    return HTMLResponse(content='<script>document.cookie="session= {}";location.href="/";</script>'.format(resp["session"]))


@app.get("/logout")
def logout(request: Request):
    session = request.cookies.get("session")
    if session is not None:
        resp = HTTPRequests.post(api + "logout", data=json.dumps({"session": session}))
    return HTMLResponse(content='<script>document.cookie="session=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";window.location="/";</script>')

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
