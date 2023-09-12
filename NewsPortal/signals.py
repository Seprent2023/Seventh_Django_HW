from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import notification


# @receiver(post_save, sender=Post)
# def news_created(sender, instance=None, **kwargs):
#     print(instance)
#     if instance is not None:
#
#         emails = User.objects.filter(
#             subscriptions__to_category=instance.category
#         ).values_list('email', flat=True)
#
#         subject = f'Новости в категории {instance.category}'
#
#         text_content = (
#             f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
#         )
#         # html_content = (
#         #     f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         #     f'Ссылка на новость</a>'
#         # )
#
#         for email in emails:
#             msg = EmailMultiAlternatives(subject, text_content, None, [email])
#             # msg.attach_alternative(html_content, "text/html")
#             msg.send()

@receiver(post_save, sender=Post)
def news_created(sender, instance=None, **kwargs):
    if instance is not None:
        notification.delay(instance_id=instance.id)
