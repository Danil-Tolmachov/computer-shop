from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail

from ComputerShop.settings import EMAIL_HOST_USER, EMAIL_VERIFICATION


def get_uid(user) -> str:
    return urlsafe_base64_encode(force_bytes(user.pk))


def get_verify_token(user) -> str:
    return token_generator.make_token(user)


def get_verify_email_message(user, template: str = 'email/verification_email.html'):
    uid = get_uid(user)
    token = get_verify_token(user)

    domain = "127.0.0.1:8000"

    message = render_to_string(template, {
        'user': user,
        'uid': uid,
        'token': token,
        'domain': domain,
    })
    return message


def send_verify_email(user, to_email: str, from_email: str = EMAIL_HOST_USER) -> None:
    mail_subject = '"ComputerShop" account verification'
    message = get_verify_email_message(user)

    if EMAIL_VERIFICATION:
        send_mail(mail_subject, message, from_email, [to_email])
    else:
        print(message)

def get_users_by_ids(ids: list) -> list:
    user_model = get_user_model()
    authors_list = []

    authors_query = user_model.objects.filter(pk__in=ids)

    for user_pk in ids:
        authors_list.append(authors_query.get(pk=user_pk))

    return authors_list
