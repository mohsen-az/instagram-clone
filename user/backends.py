from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

UserModel = get_user_model()


class OTPBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel._default_manager.get(phone_number=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_verify_code(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
