from celery import Celery

celery = Celery('anonymise', broker='redis://redis:6379', backend='redis://redis:6379', include=['anonymise.tasks'])
celery.conf.broker_url = 'redis://redis:6379'
celery.conf.result_backend = 'redis://redis:6379'

if __name__ == '__main__':
    celery.start()
