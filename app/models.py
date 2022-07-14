import logging

# 3rd parties
import peewee

# my own
from .database import (db, db_state_default)


# enable logging
logging.basicConfig(
    # filename=f"log {__name__} happy-review.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)


class ReviewQuestion(peewee.Model):
    rq_id = peewee.AutoField(null=False, primary_key=True)
    review_question = peewee.CharField(unique=True)
    rq_ts = peewee.TimestampField(default=True, resolution=3)

    class Meta:
        table_name = "review_question_table"
        database = db

    def __str__():
        return super().__str__()


class Answer(peewee.Model):
    ans_id = peewee.AutoField(null=False, primary_key=True)
    result_accuracy = peewee.CharField()
    member_support = peewee.CharField(null=True)
    turnaround_time = peewee.CharField()
    feedback = peewee.TextField(null=True)
    email = peewee.CharField(null=False, max_length=254, unique=True)
    vid_upload = peewee.CharField()
    reviewee_host = peewee.CharField(null=False, unique=True)
    reviewee_email = peewee.CharField(null=False, max_length=254, unique=True)
    # todo: ans_status can only be PENDING, COMPLETED
    ans_status = peewee.CharField(null=False, max_length=20, default="PENDING")
    answer_ts = peewee.TimestampField(default=True, resolution=3)

    class Meta:
        table_name = "answer_table"
        database = db

    def __str__(self):
        return super().__str__()
