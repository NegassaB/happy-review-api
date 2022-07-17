import logging

# 3rd parties
import peewee

# my own
from app.database import (db, db_state_default)
# from database import (db, db_state_default)


# enable logging
logging.basicConfig(
    # filename=f"log {__name__} happy-review.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)

# todo: updated everything in accordance with rq_question including crud, main and their tests


class ReviewQuestionModel(peewee.Model):
    rq_id = peewee.AutoField(null=False, primary_key=True)
    rq_question1 = peewee.CharField()
    rq_question2 = peewee.CharField()
    rq_question3 = peewee.CharField()
    rq_question4 = peewee.CharField()
    rq_question5 = peewee.CharField()
    rq_ts = peewee.TimestampField(default=True, resolution=3)

    class Meta:
        table_name = "review_question_table"
        database = db

    def __str__():
        return super().__str__()


class AnswerModel(peewee.Model):
    ans_id = peewee.AutoField(null=False, primary_key=True)
    review_question = peewee.ForeignKeyField(ReviewQuestionModel, on_delete=None, on_update="CASCADE")
    result_accuracy = peewee.CharField(null=False)
    member_support = peewee.CharField(null=True)
    turnaround_time = peewee.CharField(null=False)
    feedback = peewee.TextField(null=True)
    vid_upload = peewee.CharField(null=False)
    email = peewee.CharField(unique=True, null=False, max_length=254)
    reviewee_host = peewee.CharField(null=False, unique=True)
    # todo: ans_status can only be PENDING, COMPLETED
    ans_status = peewee.CharField(null=False, max_length=20, default="PENDING")
    answer_ts = peewee.TimestampField(default=True, resolution=3)

    class Meta:
        table_name = "answer_table"
        database = db

    def __str__(self):
        return super().__str__()
