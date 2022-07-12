from datetime import datetime
from typing import (Any, List, Union)

# 3rd parties
import pytz
import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Reviewee(BaseModel):
    reviewee_ip: str
    reviewee_email: str
    # review_ts: datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ReviewQuestion(BaseModel):
    review_question: str
    # review_question_ts = datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Answer(BaseModel):
    result_accuracy: str
    member_support: Union[str, None] = None
    turnaround_time: str
    feedback: str = None
    email: str
    vid_upload: str
    # answer_ts: datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
