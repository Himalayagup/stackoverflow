from django.dispatch import Signal, receiver
from rest_auth.views import LoginView, LogoutView

login_signal = Signal(providing_args=["context"])


class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        login_signal.send(sender=self.__class__, PING=True,user=self.request.user)
        return orginal_response

class Logout(LogoutView):
    def logout(self, request):
        try:
            request.auth.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, "REST_SESSION_LOGIN", True):
            django_logout(request)

        response = Response(
            {"detail": ("Successfully logged out.")}, status=status.HTTP_200_OK
        )
        if getattr(settings, "REST_USE_JWT", False):
            from rest_framework_jwt.settings import api_settings as jwt_settings

            if jwt_settings.JWT_AUTH_COOKIE:
                response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response
