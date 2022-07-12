from datetime import datetime
import logging
import asyncio
from typing import Iterable

# 3rd party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pytz

# my own


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


class Answer(BaseModel):
    """
    Answer: database model that will hold the answers provided by the users.
    """
    id: int = Field(default_factory=int()+1)
    result_accurancy: str
    member_support: str = None
    turnaround_time: str
    feedback: str = None
    email: str
    vid_upload: str
    answer_ts: datetime = Field(default_factory=datetime.now(tz=pytz.timezone("America/New_York")))

    @classmethod
    def all(cls, **kwargs):
        """
        all similar to Django's `all()` method, it extracts and returns all the created Answer objects as a list.

        Returns: list of all the created Answer objects
        """
        all_answers = None
        all_answers = list()
        return [all_answers.append(answer) for answer in Answer]


def get_application():
    app = FastAPI(title="happy-review-api", version='0.0.1')
    return app


app = get_application()


@app.on_event('startup')
async def startup_event():
    pass


@app.get("/answers/", response_model=Iterable[Answer])
async def read_main():
    return {"answers": Answer}
