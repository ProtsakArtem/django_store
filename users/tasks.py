from datetime import timedelta
from celery import shared_task
from django.utils.timezone import now
import uuid
from django.conf import settings
from users.models import EmailVerification, User
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email_verification(user_id):
        user = User.objects.get(id=user_id)
        expiration = now() + timedelta(days=2)
        print(f"DATA: code-{uuid.uuid4()}, user-{user}, expiration: {expiration}")
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        logger.info(f"Created email verification record: {record}")
        print("EMAIL_HOST_USER in task:", settings.EMAIL_HOST_USER)
        print("EMAIL_HOST_PASSWORD in task:", settings.EMAIL_HOST_PASSWORD)
        record.send_verification_code()
        logger.info("Celery sent email verification")
