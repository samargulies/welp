import re
from django import template
from django.template.defaultfilters import stringfilter, slugify

register = template.Library()

@register.filter
@stringfilter
def class_name(value):
	value = re.sub(r"^/", "", value)
	value = re.sub(r"/$", "", value)
	value = value.replace("/", "-")
	if not value:
		return "index"
	return slugify(value)