from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class AppTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_token_with_timestamp(self, user, timestamp: int, legacy: bool = ...) -> str:
        return {text_type(user.is_active + user.pk+ timestamp)}
        # return super()._make_token_with_timestamp(user, timestamp, legacy)

# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from six import text_type
# class AppTokenGenerator(PasswordResetTokenGenerator):

#     def _make_token_with_timestamp(self, user, timestamp) -> str:
#         return {text_type(user.is_active + user.pk+ timestamp)}
    
token_generator = AppTokenGenerator()