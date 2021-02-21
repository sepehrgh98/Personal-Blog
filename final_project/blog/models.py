from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from sqlalchemy.sql import selectable


class User(AbstractUser):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    birthdate = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=500)
    profile_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    post_date = models.DateTimeField('تاریخ انتشار', default=timezone.now)
    last_update = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    state = models.ForeignKey('Post_state', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    text = models.TextField()
    image = models.ImageField(upload_to='Post_images/', null=True, blank=True)
    category = models.ForeignKey('Post_category', on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', blank=True)

    def __str__(self):
        return self.title


class Post_state(models.Model):
    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField()
    state_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField()

    def __str__(self):
        return self.state


class Comment(models.Model):
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField()
    content = models.CharField(max_length=1000)
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user


class Tag(models.Model):
    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    name = models.CharField(max_length=200)
    post = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.name


class Post_category(models.Model):
    class Meta:
        verbose_name = 'گروه بندی پست ها'
        verbose_name_plural = 'گروه بندی های پست ها'

    name = models.CharField(max_length=200)
    super_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    last_update = models.DateTimeField()

    def __str__(self):
        return self.name
