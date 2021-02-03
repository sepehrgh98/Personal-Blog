from django.db import models
from django.utils import timezone
from django.conf import settings


class Post(models.Model):
    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
    post_date = models.DateTimeField('تاریخ انتشار',default=timezone.now)
    last_update = models.DateTimeField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='نویسنده')
    state = models.ForeignKey('Post_state', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', blank=True)
    content = models.OneToOneField('Post_content', on_delete=models.CASCADE)
    category = models.ForeignKey('Post_category', on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', blank=True)



class Post_state(models.Model):
    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    state = models.BooleanField()
    state_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField()

class Comment(models.Model):
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    last_update = models.DateTimeField()
    content = models.CharField(max_length=1000)
    comment_date = models.DateTimeField(default=timezone.now)




class Tag(models.Model):
    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'
    name = models.CharField(max_length=200)
    last_update = models.DateTimeField()


class Post_content(models.Model):
    class Meta:
        verbose_name = 'محتوا'
        verbose_name_plural = 'محتوا ها'
    title = models.CharField(max_length=500)
    text = models.TextField()
    image = models.ImageField()
    last_update = models.DateTimeField()

class Post_category(models.Model):
    class Meta:
        verbose_name = 'گروه بندی پست ها'
        verbose_name_plural = 'گروه بندی های پست ها'
    name = models.CharField(max_length=200)
    last_update = models.DateTimeField()



