from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def initial_letter_filter(text, autoescape=True):
    split_text = str.split(text, ' ')
    first_word = split_text[0]
    first_word += ' '
    other_words = ' '.join(split_text[1:])

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    result = '<strong>%s</strong>%s' % (esc(first_word), esc(other_words))
    return mark_safe(result)
