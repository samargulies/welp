from django.db.models.signals import post_save
from django.core.cache import cache
from django_comments.signals import comment_will_be_posted
from django.dispatch import receiver
from welp import settings

import json
import urllib

@receiver(post_save)
def clear_the_cache(**kwargs):
    cache.clear()
	
@receiver(comment_will_be_posted)
def verify_recaptcha(sender, **kwargs):
	print(kwargs['request'])
	
	if not kwargs['request']:
		return
	
	recaptcha_response = kwargs['request'].POST.get('g-recaptcha-response')
	url = 'https://www.google.com/recaptcha/api/siteverify'
	values = {
		'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
		'response': recaptcha_response
	}
	data = urllib.parse.urlencode(values).encode()
	req =  urllib.request.Request(url, data=data)
	response = urllib.request.urlopen(req)
	result = json.loads(response.read().decode())

	print(result)

	if not result['success']:
		return False
