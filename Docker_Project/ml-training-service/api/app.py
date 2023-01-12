import logging
from fastapi import FastAPI

logging.basicConfig(format='{asctime} {levelname:7} {message}', style='{', level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastAPI()

