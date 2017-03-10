from django.contrib.auth import get_user_model


class EmailAuthenticationBackend(object):
    """
    Backend de autentificación por medio de email.
    """

    UserModel = get_user_model()

    def authenticate(self, email=None, password=None):
        try:
            user = self.UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except self.UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.UserModel.objects.get(id=user_id)
        except self.UserModel.DoesNotExist:
            return None
