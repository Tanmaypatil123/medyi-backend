from celery import shared_task


@shared_task
def create_ai_model_for_user_and_assign(user_id:int,ai_character_id:int):
    pass