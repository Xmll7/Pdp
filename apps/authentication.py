# authentication.py (Custom authentication class)
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import Session


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            session = Session.objects.select_related('user').get(token=token)

            if session.is_expired():
                session.delete()
                raise AuthenticationFailed('Token expired')

            # Update last login
            session.last_login = timezone.now()
            session.save()

            return (session.user, token)

        except Session.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

