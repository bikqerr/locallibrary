from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def split_text_newlines(text):
    return str.splitlines(text)


@register.filter
def split_text_on_hash(text):
    return str.split(text, '#')


@register.filter
def slit_text_on_simbol(text):
    """
    :param text: the text to be split (string)
    :param simbol: the value where the text should be split
    :return: array of pjese te param: text array[]
    """
    simbol = '^^^^^^'
    return str.split(text, simbol)
