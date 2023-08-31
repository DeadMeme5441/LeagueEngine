from fastapi import FastAPI, Header, Request
from pathlib import Path
import pymongo
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(
    directory="templates", extensions=["jinja_markdown.MarkdownExtension"]
)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["league"]


@app.get("/")
async def root(request: Request):
    champ_col = mydb["champion_data"]

    champ_list = [x for x in champ_col.find({}, {"_id": 0, "name": 1})]

    context = {"request": request, "champ_list": champ_list}
    return templates.TemplateResponse("index.html", context)


@app.get("/champion_stats")
async def champion_stats(champion, request: Request):
    champ_col = mydb["champion_data"]
    champ_stats = champ_col.find_one({"name": champion}, {"_id": 0, "stats": 1})

    context = {"request": request, "champion_stats": champ_stats}
    return templates.TemplateResponse("champion_stats.html", context)


@app.get("/level/{value}/{change}")
async def level(value, change, request: Request):
    value = int(value)
    if change == "increase":
        value += 1
    if change == "decrease":
        value -= 1

    if value == 0:
        value = 1

    elif value == 19:
        value = 18

    context = {"request": request, "level": value}
    return templates.TemplateResponse("level_box.html", context)
