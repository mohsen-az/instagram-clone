from time import sleep

from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


# Task
@shared_task(name="send phone verification code", queue="high")
def send_phone_verification_code(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    sleep(10)
    # TODO: Send sms
    return f"Verification code send to user: {user.username}({user.phone_number})."


@shared_task(name="send email verification link")
def send_email_verification_link(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    sleep(10)
    # TODO: Send email
    return f"Link send to user: {user.username}({user.email})."


# Periodic Task
@shared_task(name="run every 5 second", queue="low")
def run_every_5_second():
    return f"Run Every 5 Second..."


@shared_task(name="notify unverified users", queue="mid")
def check_unverified_users():
    """
    for user in User.objects.all():
        if not user.verified:
            send_email_verification_link.delay(user.username)
            send_phone_verification_code.delay(user.username))
    """
    pass
