from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.translation import gettext_lazy as _

from rest_auth.models import ConfirmEmailToken, User

from jobs.tasks import send_multi_alternative

new_user_registered = Signal(
    providing_args=['user_id'],
)

new_order = Signal(
    providing_args=['user_id'],
)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """

    send_multi_alternative.delay(
        _('Сброс пароля для {}').format(reset_password_token.user),
        _('Токен для сброса пароля {}').format(reset_password_token.key),
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    Отправляем письмо с подтрердждением почты
    """
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    send_multi_alternative.delay(
        _('Подтверждение регистрации в магазине для {}').format(token.user.email),
        _('Токен для подтверждения регистрации {}').format(token.key),
        settings.EMAIL_HOST_USER,
        [token.user.email]
    )


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    Отправяем письмо при изменении статуса заказа
    """
    user = User.objects.get(id=user_id)

    send_multi_alternative.delay(
        _('Обновление статуса заказа'),
        _('Заказ сформирован'),
        settings.EMAIL_HOST_USER,
        [user.email]
    )
