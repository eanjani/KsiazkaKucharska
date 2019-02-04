from django import template
from django.utils.safestring import mark_safe
import codecs

register = template.Library()
encoding = "utf-8"
on_error = "replace"

@register.filter(name='boldText')
def boldText(value, args):
	tags = set(args.split(','))
	for tag in tags:
		value = value.replace(tag, "<font color='blue'>"+tag+"</font>")
	return mark_safe(value)