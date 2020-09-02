from django.utils.translation import gettext_lazy as t
from rest_framework.permissions import BasePermission


class IsShop(BasePermission):
    """
    Permission class
    Проверка, что пользователь имеет тип shop
    """

    message = t('Только для магазинов')

    def has_permission(self, request, view):
        return request.user.type == 'shop'


class IsBuyer(BasePermission):
    """
    Permission class
    Проверка, что пользователь имеет тип buyer
    """

    message = t('Только для покупателей')

    def has_permission(self, request, view):
        return request.user.type == 'buyer'
