from abc import ABC, abstractmethod, abstractproperty
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail

from ComputerShop.settings import EMAIL_HOST_USER, EMAIL_VERIFICATION, DOMAIN



class VerifyMessage(ABC):

    @abstractproperty
    def template():
        pass

    def __init__(self):
        self.message = str

    @abstractmethod
    def create(self) -> str:
        pass

    @staticmethod
    def get_uid(user) -> str:
        # Returns user uid
        return urlsafe_base64_encode(force_bytes(user.pk))

    @staticmethod
    def get_verify_token(user) -> str:
        return token_generator.make_token(user)


class VerifyEmailMessage(VerifyMessage):
    template = 'email/verification_email.html'

    def __init__(self, user):
        super().__init__()
        self.user = user

    def create(self):

        uid = self.get_uid(self.user)
        token = self.get_verify_token(self.user)
        domain = DOMAIN

        self.message = render_to_string(self.template, {
            'user': self.user,
            'uid': uid,
            'token': token,
            'domain': domain,
        })

        return self.message


class VerifyPasswordMessage(VerifyMessage):
    template = 'email/verification_new_password.html'

    def __init__(self, user):
        super().__init__()
        self.user = user

    def create(self):

        uid = self.get_uid(self.user)
        token = self.get_verify_token(self.user)
        domain = DOMAIN

        self.message = render_to_string(self.template, {
        'user': self.user,
        'uid': uid,
        'token': token,
        'domain': domain,
        })

        return self.message


def send_verify_email(user, to_email: str, from_email: str = EMAIL_HOST_USER) -> None:

    mail_subject = 'Account verification'
    message = VerifyEmailMessage(user).create()

    if EMAIL_VERIFICATION:
        send_mail(mail_subject, message, from_email, [to_email])


def send_change_password_email(user, to_email: str, from_email: str = EMAIL_HOST_USER) -> None:

    mail_subject = 'Change password'
    message = VerifyPasswordMessage(user).create()

    send_mail(mail_subject, message, from_email, [to_email])


def get_users_by_ids(ids: list) -> list:

    user_model = get_user_model()
    authors_list = []

    authors_query = user_model.objects.filter(pk__in=ids)

    # Make author list
    for user_pk in ids:
        authors_list.append(authors_query.get(pk=user_pk))

    return authors_list
