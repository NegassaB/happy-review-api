from datetime import datetime
import logging
from typing import (Iterable, List)

# 3rd party imports
from fastapi import (FastAPI, Header, HTTPException, Request, status)
import pytz

# my own
from .schemas import (Reviewee, ReviewQuestion, Answer)
# from schemas import (Reviewee, ReviewQuestion, Answer)

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} happy-review.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)

# todo: access IP address from the request
# todo: get called when `submit review` button is called on the UI
# todo: use sqlite for storing answers & user email
# todo: check user email in sqlite for re-submission
# todo: build upload feature that will store the user uploaded video in a folder named `upload` and it's address in db
# todo: name each uploaded video with user email + name
# todo: deploy on digital ocean


def get_application():
    app = FastAPI(title="happy-review-api", version='0.0.1')
    return app


app = get_application()

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
