import peewee

from .database import db


class Reviewee(peewee.Model):
    r_id = peewee.AutoField(null=False, primary_key=True)
    r_ip = peewee.CharField(null=False)
    r_email = peewee.CharField(null=False, max_length=254)
    r_ts = peewee.TimestampField(default=True, resolution=3)

    class Meta:
        table_name = "reviewee_table"
        database = db

    def __str__():
        return super().__str__()


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
    email = peewee.CharField()
    vid_upload = peewee.CharField()
    reviwee = peewee.ForeignKeyField(
        Reviewee,
        backref="responding_user",
        on_delete=None,
        to_field="r_email",
        on_update="CASCADE"
        )
    ans_status = peewee.CharField(null=False, max_length=20, default="PENDING")
    answer_ts = peewee.TimestampField(default=True, resolution=3)

    class Meta:
        table_name = "answer_table"
        database = db

    def __str__(self):
        return super().__str__()
