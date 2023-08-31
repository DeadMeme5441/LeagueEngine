import sys
import pymongo
import requests
import tarfile
from pathlib import Path
import json
import time


def get_latest_data_dump(url):
    r = requests.get(url, allow_redirects=True)
    with open("data.tgz", "wb") as f:
        f.write(r.content)


def update_data_dump():
    data_tar = tarfile.open("data.tgz")
    data_tar.extractall("./data")
    data_tar.close()


def update_mongo_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["league"]

    champcol = mydb["champion_data"]
    champcol.drop()

    champion_files = Path("./data/13.16.1/data/en_US/champion/").glob("*")

    for champion in champion_files:
        f = dict(json.load(open(str(champion))))
        champcol.insert_one(f["data"][str(champion).split("/")[-1].split(".")[0]])

    itemcol = mydb["items_data"]
    itemcol.drop()

    item_file = "./data/13.16.1/data/en_US/item.json"

    f = dict(json.load(open(item_file)))

    for item in f["data"]:
        itemcol.insert_one(f["data"][item])


def get_stats_images():
    stats = [
        {
            "name": "HP",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/5/5f/Health_icon_2.png/revision/latest?cb=20181210112020",
        },
        {
            "name": "MP",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/0/0a/Ability_power_colored_icon.png/revision/latest?cb=20210221222133",
        },
        {
            "name": "MoveSpeed",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/2/21/Movement_speed_colored_icon.png/revision/latest?cb=20210221222257",
        },
        {
            "name": "Armor",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/d/d5/Armor_colored_icon.png/revision/latest?cb=20210221222141",
        },
        {
            "name": "MagicResist",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/a/a3/Magic_resistance_colored_icon.png/revision/latest?cb=20210221222244",
        },
        {
            "name": "AttackRange",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/1/1c/Range_colored_icon.png",
        },
        {
            "name": "CriticalChance",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/3/3e/Critical_strike_chance_colored_icon.png",
        },
        {
            "name": "AttackDamage",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/7/7e/Attack_damage_colored_icon.png",
        },
        {
            "name": "AttackSpeed",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/4/49/Attack_speed_colored_icon.png",
        },
        {
            "name": "AbilityPower",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/0/0a/Ability_power_colored_icon.png",
        },
        {
            "name": "AbilityHaste",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/7/7b/Cooldown_reduction_icon_2.png",
        },
        {
            "name": "ArmorPenetration",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/6/64/Armor_penetration_colored_icon.png",
        },
        {
            "name": "ArmorPenetration",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/6/64/Armor_penetration_colored_icon.png",
        },
        {
            "name": "MagicPenetration",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/f/f8/Magic_penetration_colored_icon.png",
        },
        {
            "name": "HealthRegen",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/a/a9/Health_regeneration_colored_icon.png",
        },
        {
            "name": "Lifesteal",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/6/6b/Life_steal_colored_icon.png",
        },
        {
            "name": "Omnivamp",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/a/a7/Omnivamp_colored_icon.png",
        },
        {
            "name": "OnHit",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/7/75/On-hit_icon.png",
        },
        {
            "name": "Gold",
            "url": "https://static.wikia.nocookie.net/leagueoflegends/images/1/10/Gold.png",
        },
    ]

    for stat in stats:
        with open("./static/StatImages/" + stat["name"] + ".png", "wb") as outfile:
            r = requests.get(stat["url"])
            outfile.write(r.content)


def write_champ_data(path, data):
    with open(path, "wb") as f:
        f.write(data)


def get_champ_stats():
    url = "https://raw.communitydragon.org/latest/cdragon/files.exported.txt"

    with open("files.txt", "wb") as out:
        r = requests.get(url)
        out.write(r.content)

    url = "https://raw.communitydragon.org/latest/"
    paths = []

    with open("files.txt", "r") as f:
        for line in f:
            if (
                "/data/characters/" in line
                and ".bin.json" in line
                and "skin" not in line
            ):
                # time.sleep(2)
                query_path = url + line.strip()
                print(query_path)
                r = requests.get(query_path)
                file_path = "./static/champ_data/" + line.split("/")[-1]
                write_champ_data(file_path.strip(), r.content)


def update_mongo_base_champ_data():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["league"]
    champ_base_col = mydb["base_data"]
    champ_names = mydb["champ_list"]

    champ_base_col.drop()
    champ_names.drop()

    paths = Path("./static/champ_data/").glob("*")

    for path in paths:
        f = open(str(path))
        data = dict(json.load(f))
        champ_name = ""
        for key in data.keys():
            if "Characters" in key:
                champ_name = key.split("/")[1]
                break
        champ_base_data = {}
        champ_base_data["champ_name"] = champ_name
        champ_base_data["data"] = data
        champ_base_col.insert_one(champ_base_data)
        champ_names.insert_one({"name": champ_name})
        f.close()


if __name__ == "__main__":
    update_mongo_base_champ_data()
# get_latest_data_dump(
#     "https://ddragon.leagueoflegends.com/cdn/dragontail-13.16.1.tgz"
# )
# update_data_dump()
# update_mongo_db()
# check_move_speed()
