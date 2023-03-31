from typing import Union
from fastapi import FastAPI,requests,Request,Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

@app.get("/")
def home(request: Request):
    username = request.cookies.get("username")
    if username:
        print("returning user: "+username)
        return templates.TemplateResponse("homePage.html", {"request": request, "username": username})
    return templates.TemplateResponse("login.html", {"request": request,"val":"hello!"})
@app.post("/")
async def login(response:Response,request: Request):
    frm=await request.form()
    response.set_cookie(key="username", value=frm["username"])
    return templates.TemplateResponse("homePage.html", {"request": request,"username":frm["username"]})
@app.get("/logout")
def logout(response: Response):
    response.delete_cookie("username")
    return HTMLResponse(content='<meta http-equiv="refresh" content="0; URL=/" />')

if __name__ == "__main__":
    uvicorn.run(app, host="fluidos.anonyo.net", port=5800)