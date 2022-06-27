import datetime
import logging
import asyncio

# 3rd party imports
from fastapi import FastAPI, HTTPException

# my own


# enable logging
logging.basicConfig(
    # filename=f"log {__name__} ReviewerBot.log",
    format='%(asctime)s - %(ascName)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# get logger
logger = logging.getLogger(__name__)

# todo: access IP address from the request
# todo: use google forms API for questions
# todo: use google sheets API for storing answers & user email
# todo: check user email in sheets for re-submission
# todo: build upload feature that will store the user uploaded video in a folder named `upload`
# todo: name each uploaded video with user email + name
# todo: deploy on digital ocean
