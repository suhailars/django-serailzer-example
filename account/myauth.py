from django.conf import settings
#from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from account.models import AppUser

class FBBackend(object):
    def authenticate(self, fb_id=None):
        try:
            user = AppUser.objects.get(fb_id=fb_id)
        except AppUser.DoesNotExist:
            return None
        return user.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None