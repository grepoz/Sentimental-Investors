import json
from scrap_manager import process_scrap_request
from scraper.param_manager import Asset
from utilities.time_manager import TimeManager
import winsound


# first check if asset has that long history
start_time = TimeManager.create_rcf_3339_timestamp(2014, 1, 1)
end_time = TimeManager.create_rcf_3339_timestamp(2022, 11, 17)

request_data = []
f = open('scraper/assets.json')
data = json.load(f)
for attribute, value in data.items():
    request_data.append((Asset(value, attribute), start_time, end_time))

for tup in request_data:
    process_scrap_request(tup[0], tup[1], tup[2])

for i in range(3):
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
