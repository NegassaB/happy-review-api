import logging
from typing import (List)

# 3rd party imports
from fastapi import (Depends, FastAPI, Header, HTTPException, Request, status, Response)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# my own
from app.schemas import (ReviewQuestionSchema, AnswerSchema)
from app.crud import (
    create_db_tables,
    open_db_cxn,
    close_db_cxn,
    get_reviewee_host,
    create_answer,
    get_single_answer,
    all_answers
)
from app.database import (db, db_state_default)
# from schemas import (ReviewQuestionSchema, AnswerSchema)
# from crud import (
#     create_db_tables,
#     open_db_cxn,
#     close_db_cxn,
#     get_reviewee_host,
#     create_answer,
#     get_single_answer,
#     all_answers
# )
# from database import (db, db_state_default)

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} happy-review.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)

# todo: get called when `submit review` button is called on the UI
# todo: build upload feature that will store the user uploaded video in a folder named `upload` and it's address in db
# todo: name each uploaded video with user email + name
# todo: deploy on digital ocean
# todo: Update questions via ReviewQuestion model
# todo: display questions & answers on Admin dashboard


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    """
    get_db connect the database right at the beginning of a request and disconnect it at the end.

    Args:
        db_state (_type_, optional): _description_. Defaults to Depends(reset_db_state).
    """
    try:
        open_db_cxn()
        yield
    finally:
        if not db.is_closed():
            close_db_cxn()


def get_application():
    app = FastAPI(title="happy-review-api", version='0.0.1')
    return app


app = get_application()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")
# templates = Jinja2Templates(directory="templates")


@app.on_event('startup')
async def startup_event():
    create_db_tables()


@app.post("/answers/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_db)])
async def insert_answer(answer: AnswerSchema, request: Request):
    reviewee_host = request.client.host
    if not reviewee_host:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="IP was not provided"
        )
    if get_reviewee_host(reviewee_host) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no IP provided or the IP already exists in the system"
        )

    try:
        create_answer(answer, reviewee_host)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"{e}"
        )
    else:
        return {"status": "successfully saved answer", "IP": reviewee_host}


@app.get("/answers/{answer_id}", status_code=status.HTTP_200_OK, response_model=AnswerSchema, dependencies=[Depends(get_db)])
async def get_an_answer(answer_id: int):
    answer = get_single_answer(id=answer_id)
    return answer


@app.get("/answers/", status_code=status.HTTP_200_OK, response_model=List[AnswerSchema], dependencies=[Depends(get_db)])
async def get_all_answers():
    answers = all_answers()
    return answers


@app.get("/dashboard", response_class=HTMLResponse, status_code=200)
async def dashboard(request: Request):
    answers = all_answers()
    return templates.TemplateResponse("dashboard.html", {"request": request, "answers": answers})
