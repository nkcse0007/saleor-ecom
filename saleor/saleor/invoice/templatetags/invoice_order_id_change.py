from django import template

register = template.Library()


def order_id_change(token):
    """Removes all values of arg from the given string"""
    return str(token.split("-")[0] + "0").upper()


register.filter('order_uid', order_id_change)
