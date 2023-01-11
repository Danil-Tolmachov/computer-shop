
from abc import ABC, abstractmethod
from typing import Union

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.core.validators import validate_email


class BaseValidator(ABC):
    
    @staticmethod
    @abstractmethod
    def validate(request, password, **fields) -> bool:
        pass



class EmailValidator(BaseValidator):

    @staticmethod
    def validate(request, password, **fields) -> bool:

        old_email = fields['old_email']
        new_email1 = fields['new_email1']
        new_email2 = fields['new_email2']

        if new_email1 == None:
            raise SuspiciousOperation('Fill in the new email field')

        if not new_email1 == new_email2:
            raise SuspiciousOperation('Check new email confirmation field')
        
        if authenticate(email=old_email, password=password) is None:
            raise SuspiciousOperation('Invalid password was provided')

        if old_email == new_email1:
            raise SuspiciousOperation('Enter a new email, not the old one')

        if authenticate(email=new_email1, password=password) is not None:
            raise SuspiciousOperation('That email is already used')

        try:
            validate_email(new_email1)
        except ValidationError:
            raise SuspiciousOperation('Invalid email')
            
            

class PasswordValidator(BaseValidator):

    @staticmethod
    def validate(request, password, **fields) -> bool:
        
        email = request.user.email
        new_password1 = fields['new_password1']
        new_password2 = fields['new_password2']

        if new_password1 == None:
            raise SuspiciousOperation('Fill in the new password field')

        if not new_password1 == new_password2:
            raise SuspiciousOperation('Check new new password confirmation field')
        
        if authenticate(email=email, password=password) is None:
            raise SuspiciousOperation('Invalid current password was provided')

        if password == new_password1:
            raise SuspiciousOperation('Enter a new password, that differ from the old one')

        try:
            validate_password(password=new_password1)
        except ValidationError:
            raise SuspiciousOperation('You shoud use stronger password')