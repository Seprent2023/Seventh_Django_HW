from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
	author = models.OneToOneField(User, on_delete=models.CASCADE)
	rating_author = models.IntegerField(default=0)

	def update_rating(self):
		author_post_rating = self.post_set.aggregate(sum_post_rating=Sum('rating'))
		post_rating = author_post_rating.get('sum_post_rating')

		author_comment_rating = self.comment_set.aggregate(sum_comment_rating=Sum('rating'))
		comment_rating = author_comment_rating.get('sum_comment_rating')

		author_comm_post_rating = self.post_set.aggregate(sum_comm_post_rating=Sum('rating'))
		comm_post_rating = author_comm_post_rating.get('sum_comm_post_rating')

		self.rating_author = post_rating * 3 + comment_rating + comm_post_rating
		self.save()


class Category(models.Model):
	# GENERAL = 'GEN'
	# MOVIE = 'MOV'
	# MUSIC = 'MUS'
	# BOOKS = 'BKS'
	# POLITICS = 'PLT'
	#
	# CATEGORY_CHOISE = [
	# 	(GENERAL, 'Общая'),
	# 	(MOVIE, 'Кино'),
	# 	(MUSIC, 'Музыка'),
	# 	(BOOKS, 'Книги'),
	# 	(POLITICS, 'Политика'),
	#
	# ]
	name = models.CharField(max_length=30, unique=True)
	subscriber = models.ManyToManyField(User, through='Subscription')

	def __str__(self):
		return self.name.title()


class Post(models.Model):
	article = 'AR'
	news = 'NW'

	TYPE = [
		(article, 'Статья'),
		(news, 'Новость')
	]

	type_post = models.CharField(max_length=2, choices=TYPE, default='NW')
	time_in = models.DateTimeField(auto_now_add=True)
	headline = models.CharField(max_length=128,)
	text = models.TextField()
	rating = models.IntegerField(default=0)
	to_author = models.ForeignKey(Author, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='n', default='GEN')


	def preview(self):
		return self.text[:20] + '...'
		# return f'{self.text[0:2] + "..."}'
		# return '{}'.format(self.text[0:128] + '...')

	def like_post(self):
		self.rating += 1
		self.save()

	def dislike_post(self):
		self.rating -= 1
		self.save()

	def __str__(self):
		return f'{self.headline}: {self.text[:20]}'

	def get_absolute_url(self):
		return reverse('post_detail', args=[str(self.id)])


# class PostCategory(models.Model):
# 	to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
# 	to_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
	text = models.TextField()
	time_in = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)
	comm_post = models.ForeignKey(Post, on_delete=models.CASCADE)
	comm_user = models.ForeignKey(User, on_delete=models.CASCADE)

	def like_comm(self):
		self.rating += 1
		self.save()

	def dislike_comm(self):
		self.rating -= 1
		self.save()


class Subscription(models.Model):
	user = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name='subscriptions',
	)
	to_category = models.ForeignKey(
		to=Category,
		on_delete=models.CASCADE,
		related_name='subscriptions',
	)
