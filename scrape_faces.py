import datetime
import time
import re
import requests
import json
import os


def duck_req(keywords):
    param = {"q": keywords}
    print("Hitting DuckDuckGo for Token")

    # make request to obtain unique token for search query
    time.sleep(2)
    res = requests.post(base_url, data=param)
    search_obj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)
    if not search_obj:
        print("Token Parsing Failed")
        return -1

    print("Token Obtained")

    params = (
        ('l', 'wt-wt'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', search_obj.group(1)),
        ('f', ',,,'),
        ('p', '2')
    )

    search_url = base_url + "i.js"

    try:
        time.sleep(2)
        res = requests.get(search_url, headers=headers, params=params)
        data = json.loads(res.text)
        get_image(data["results"], keywords)
    except ValueError as e:
        print("Error.: " + str(e) + " \nPlease try again.")


def get_image(objs, keyword):
    # Check directory exists
    if not os.path.isdir("DataSet/" + keyword + "/"):
        os.mkdir("DataSet/" + keyword + "/")

    img_links = [obj['image'] for obj in objs]

    for i, link in enumerate(img_links):
        # time.sleep(2)
        try:
            req = requests.get(link)
        except:
            print("Skipping link " + str(i))
            continue

        if not req.status_code == 200:
            continue
        file = keyword.replace(" ", "") + "_" + str(i) + ".jpg"
        filename = "DataSet/" + keyword + "/" + file

        # save image
        with open(filename, "wb+") as f:
            f.write(req.content)

        print("File: " + filename + " saved succesfully.")


# Start Time:
start_time = time.time()
# Today:
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Image class tag
# tag = "tile--img__img  js-lazyload"

# List of actors to search for
actors = ["Michael Cera", "Aubrey Plaza", "Alison Pill", "Brie Larson", "Ellen Wong", "Jason Schwartzman",
          "Johnny Simmons", "Mark Webber", "Mary Elizabeth Winstead", "Nelson Franklin"]

# Defaults values
headers = {
        'dnt': '1',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'x-requested-with': 'XMLHttpRequest',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6,ms;q=0.4',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://duckduckgo.com/',
        'authority': 'duckduckgo.com',
    }

base_url = "https://duckduckgo.com/"


for actor in actors:
    duck_req(actor)


print("scrape_faces.py took {} seconds to run".format(time.time()-start_time))
