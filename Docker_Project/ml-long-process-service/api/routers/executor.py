from fastapi import HTTPException
import logging

def init_routes(app, executor_maker):
    global executor
    executor = executor_maker()
    @app.post("/task")
    def start_task():
        global executor
        state = executor.get_state()
        if state == 'Done':
            logging.info('Previous executor done. Initiating new.')
            executor = executor_maker()
            executor.start()
        elif state == 'Standby':
            executor.start()
            logging.info('Executor on standby found. Starting job.')
        else:
            logging.info('Job in progress. Executor working.')
            return {"message": "Job in progress. Wait until done.", "status": state}
        return {"message": "Job Created, check status after some time."}

    @app.get("/status")
    def status():
        global executor
        state = executor.get_state()
        logging.debug(f'Retrieved executor state: {state}')
        return {"status": state}
