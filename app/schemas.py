from datetime import datetime
from typing import (Any, List, Union)

# 3rd parties
import pytz
import peewee
from pydantic import BaseModel as BaseSchema
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict): # seems like it serializes db output against pydantic schemas for individual results & converts to a list when it's gross results
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ReviewQuestionSchema(BaseSchema):
    review_question: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class AnswerSchema(BaseSchema):
    result_accuracy: str
    member_support: Union[str, None] = None
    turnaround_time: str
    feedback: Union[str, None] = None
    vid_upload: str
    email: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
