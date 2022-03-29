from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth.models import User
#from .models import Profile


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp)
        )

account_activation_token = AccountActivationTokenGenerator()