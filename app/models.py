import peewee

from .database import db


class Answer(peewee.Model):
    ans_id = peewee.AutoField(null=False, primary_key=True)
    result_accurancy = peewee.CharField()
    member_support = peewee.CharField(null=True)
    turnaround_time = peewee.CharField()
    feedback = peewee.TextField(null=True)
    email = peewee.CharField()
    vid_upload = peewee.CharField()
    answer_ts = peewee.TimestampField(default=True, resolution=3)

    class Meta:
        table_name = "answer_table"
        database = db

    def __str__(self):
        return super().__str__()
