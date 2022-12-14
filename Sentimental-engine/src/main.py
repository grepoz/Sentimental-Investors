import json

from flask import Flask, request
from threading import Thread

from request_models import ScrapParams, UserScrapParams
from scrap_manager import process_scrap_request
from scraper.param_manager import Asset

app = Flask(__name__)


@app.post("/scrap-tweets")
def scrap_tweets():
    data = ScrapParams.parse_obj(request.json)
    app.logger.debug("requested endpoint: /scrap-tweets")

    return process_scrap_request(
            Asset(data.asset_name, data.token),
            data.start_time,
            data.end_time,
            data.query)


@app.post("/user-scrap-tweets")
def user_scrap_tweets():
    data = UserScrapParams.parse_obj(request.json)
    app.logger.debug("requested endpoint: /user-scrap-tweets")
    thread_for_processing_scrap_request = Thread(target=process_scrap_request_task, args=[data])
    thread_for_processing_scrap_request.start()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def process_scrap_request_task(data):
    process_scrap_request(Asset(
        data.asset_name,
        data.token),
        data.start_time,
        data.end_time,
        data.query,
        data.bearer_token,
        data.email)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
