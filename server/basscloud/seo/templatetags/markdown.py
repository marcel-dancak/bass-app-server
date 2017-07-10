from django import template
from markdown2 import Markdown

register = template.Library()


@register.filter
def md2html(value):
    markdowner = Markdown()
    return markdowner.convert(value)
