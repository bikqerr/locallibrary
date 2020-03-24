import datetime
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


@register.filter
def cut(value, arg):
    """
    Removes all values of arg from the given string
    """
    return value.replace(arg, '')


@register.filter(expected_localtime=True)
def businesshours(value):
    try:
        return 9 <= value.hour < 17
    except AttributeError:
        return 'Error'


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag(takes_context=True)
def info_context(context):
    return context


@register.inclusion_tag('tag_template/all_books_per_author_tag.html')
def books_per_author(author):
    books = author.book_set.all()
    return {'books': books}


@register.inclusion_tag('tag_template/list_borrowed_all_tag.html', takes_context=True)
def list_borrowed_all(context):
    return context

