from django.conf.global_settings import EMAIL_HOST
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail

from ComputerShop.settings import EMAIL_HOST_USER


def get_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))


def get_verify_token(user):
    return token_generator.make_token(user)


def send_verify_email(user, to_email, template='email/verification_email.html', from_email=EMAIL_HOST_USER):

    uid = get_uid(user)
    token = get_verify_token(user)

    mail_subject = '"ComputerShop" account verification'

    message = render_to_string(template, {
        'user': user,
        'uid': uid,
        'token': token,
        'domain': "127.0.0.1:8000",
    })

    send_mail(mail_subject, message, from_email, [to_email])
