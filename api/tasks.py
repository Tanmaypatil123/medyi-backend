from celery import  shared_task

@shared_task
def tryfun():
    print("hellllll")