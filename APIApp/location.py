from typing import List

import requests as HTTPRequests
import json

from dbHandler2 import Connect
from models.models import User, Coordinates,Location

api="http://ip-api.com/json/{}"
def getInfo(ip:str):
    if ip== "127.0.0.1":
        ip=""
    return json.loads(HTTPRequests.get(api.format(ip)).text)

def getLocations(user:User,con:Connect)->List[Location]:
    resp=[]
    for i in user.coordinates:
        resp.append(Location(id=i.id,name=i.name))
    return resp
def getCoordinates(id: int, user: User, con: Connect) -> Coordinates | None:
    for i in user.coordinates:
        if i.id == id:
            return i
    return None