from celery import shared_task
import datetime
from NewsPortal.models import Post
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.contrib.auth.models import User


@shared_task
def my_task(*args, **kwargs):
	today = datetime.datetime.now()
	last_week = today - datetime.timedelta(days=7)
	posts = Post.objects.filter(time_in__gte=last_week)
	# text = '\n'.join(['{} - {} - {}'.format(p.headline, p.category, f'http://127.0.0.1:8000{p.get_absolute_url()}') for p in posts])
	text = '\n'.join(['{} - {}'.format(p.headline, f'http://127.0.0.1:8000{p.get_absolute_url()}') for p in posts])
	mail_managers('Самые последние новости', text)


@shared_task
def notification(instance_id):
	instance = Post.objects.get(pk=instance_id)
	if instance is not None:
		emails = User.objects.filter(
			subscriptions__to_category=instance.category
		).values_list('email', flat=True)
		subject = f'Новости в категории {instance.category}'
		text_content = (
			f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
		)
		for email in emails:
			msg = EmailMultiAlternatives(subject, text_content, None, [email])
			msg.send()
