from datetime import datetime
import logging
from typing import (Iterable, List)
import os
import sys

# 3rd party imports
from fastapi import (FastAPI, Header, HTTPException, Request, status)
import pytz
from pydantic import BaseSettings

# my own
# from .schemas import (Reviewee, ReviewQuestion, Answer)
from schemas import (Reviewee, ReviewQuestion, Answer)

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} happy-review.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)

# todo: get called when `submit review` button is called on the UI
# todo: use sqlite for storing answers & user email
# todo: check user email in sqlite for re-submission
# todo: build upload feature that will store the user uploaded video in a folder named `upload` and it's address in db
# todo: name each uploaded video with user email + name
# todo: deploy on digital ocean


class Settings(BaseSettings):
    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()

def init_webhooks(base_url):
    pass


def get_application():
    app = FastAPI(title="happy-review-api", version='0.0.1')
    return app


app = get_application()

if settings.USE_NGROK:
    from pyngrok import ngrok

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    settings.BASE_URL = public_url
    init_webhooks(public_url)

fake_db: List[str] = []


@app.on_event('startup')
async def startup_event():
    pass


@app.post("/answers/", status_code=status.HTTP_201_CREATED)
async def insert_answer(answer: Answer, request: Request):
    # todo: call db function to save here, till then keep in memory
    client_host = request.client.host
    fake_db.append(answer)
    return {"status": "successfully saved answer", "IP": client_host}


@app.get("/answers/", response_model=Answer)
async def read_main():
    return {"answers": Answer}
