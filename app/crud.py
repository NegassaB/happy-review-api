import logging

# 3rd party
import peewee

# my own
from .models import (Answer, ReviewQuestion)
from . import schemas
from .database import (db, db_state_default)

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} happy-review.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)


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
        tbl_list.append(ReviewQuestion)
    if not db.table_exists("answer_table"):
        tbl_list.append(Answer)

    try:
        db.create_tables(tbl_list)
    except peewee.PeeweeException as pex:
        logger.exception(f"PeeweeException occurred -- {pex}", exc_info=True)
        raise pex
    except Exception as e:
        logger.exception(f"Excpetion occurred -- {e}", exc_info=True)
        raise e
    else:
        logger.info("successfully created db tables")
    finally:
        close_db_cxn()


def get_reviewee_host(host: str):
    return Answer.filter(Answer.reviewee_host == host).first()


def get_reviewee_email(email: str):
    return Answer.filter(Answer.reviewee_email == email).first()


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
