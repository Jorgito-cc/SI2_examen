from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .utils import log_action

@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    log_action(user, "Inicio de sesión", request)

@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    log_action(user, "Cierre de sesión", request)
