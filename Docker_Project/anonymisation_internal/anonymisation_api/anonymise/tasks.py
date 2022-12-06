import json

from worker import celery
from training.run_ner import main
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
@celery.task(bind=True)
def train(id):
    logger.info("started training")
    try:
        main()
    except Exception as e:
        print(e)
        logger.info(e)
    logger.info("training ended")
    return json.dumps({'message':'started training', 'code':'SUCCESS'})

