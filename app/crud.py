import logging

# 3rd party
import peewee

# my own
from app.models import (AnswerModel, ReviewQuestionModel)
from app.schemas import AnswerSchema as AnswerSchema
from app.database import (db, db_state_default)
# from models import (AnswerModel, ReviewQuestionModel)
# from schemas import AnswerSchema
# from database import (db, db_state_default)

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} happy-review.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)


def default_exception(exception):
    logger.exception(f"Exception occurred -- {exception}", exc_info=True)
    raise exception


def open_db_cxn():
    if db.is_closed():
        db.connect(reuse_if_open=True)
        logger.info("database connection established")


def close_db_cxn():
    if not db.is_closed():
        db.close()
        logger.info("database connection closed")


def create_db_tables():
    open_db_cxn()
    tbl_list = []
    if not db.table_exists("review_question_table"):
        tbl_list.append(ReviewQuestionModel)
    if not db.table_exists("answer_table"):
        tbl_list.append(AnswerModel)

    try:
        db.create_tables(tbl_list)
    except peewee.PeeweeException as pex:
        logger.exception(f"PeeweeException occurred -- {pex}", exc_info=True)
        raise pex
    except Exception as e:
        default_exception(e)
    else:
        logger.info("successfully created db tables")
    finally:
        close_db_cxn()


def get_reviewee_host(host: str):
    try:
        return AnswerModel.filter(AnswerModel.reviewee_host == host).first()
    except Exception as e:
        logger.exception(f"Exception occurred -- {e}", exc_info=True)
        return None


def create_answer(answer: AnswerSchema, host: str):
    if len(answer.result_accuracy) > 1 and len(answer.turnaround_time) > 1 and len(answer.vid_upload) > 1 and len(answer.email) > 1:
        try:
            return AnswerModel(**answer.dict(), reviewee_host=host).save()
        except Exception as e:
            default_exception(e)
    else:
        default_exception(Exception("one or more of the required fields is empty"))


def get_single_answer(id: int):
    try:
        return AnswerModel.filter(AnswerModel.ans_id == id).first()
    except Exception as e:
        default_exception(e)


def all_answers(skip: int = 0, limit: int = 1000):
    try:
        return list(AnswerModel.select().offset(skip).limit(limit))
    except Exception as e:
        default_exception(e)


# def get_user(user_id: int):
#     return models.User.filter(models.User.id == user_id).first()


# def get_user_by_email(email: str):
#     return models.User.filter(models.User.email == email).first()


# def get_users(skip: int = 0, limit: int = 100):
#     return list(models.User.select().offset(skip).limit(limit))


# def create_user(user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db_user.save()
#     return db_user


# def get_items(skip: int = 0, limit: int = 100):
#     return list(models.Item.select().offset(skip).limit(limit))


# def create_user_item(item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db_item.save()
#     return db_item
