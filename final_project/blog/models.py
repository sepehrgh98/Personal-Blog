from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tmc
from image_cropping import ImageRatioField, ImageCropField


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    birthdate = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    last_update = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=500, unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    profile_image = models.ImageField(upload_to='user_images', null=True, blank=True, default='default/udefault.png')
    cropping = ImageRatioField('profile_image', '430x360', size_warning=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Post(models.Model):
    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    post_date = models.DateTimeField('تاریخ انتشار', default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    title = models.CharField(max_length=500)
    text = tmc.HTMLField()
    image = models.ImageField(upload_to='Post_images/', null=True, blank=True, default='default/pdefault.png')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Like(models.Model):
    class Meta:
        verbose_name = 'پسندیدم'
        verbose_name_plural = 'پسندیدم ها'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} , {self.post}"


class Dislike(models.Model):
    class Meta:
        verbose_name = 'نپسندیدم'
        verbose_name_plural = 'نپسندیدم ها'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} , {self.post}"


class Comment(models.Model):
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    comment_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text


class Tag(models.Model):
    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    name = models.CharField(max_length=200)
    post = models.ManyToManyField('Post', through="Post_Tag", null=True, blank=True, related_name="myTags")

    def __str__(self):
        return self.name


class Post_Tag(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Category(models.Model):
    class Meta:
        verbose_name = 'گروه بندی پست ها'
        verbose_name_plural = 'گروه بندی های پست ها'

    name = models.CharField(max_length=200, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
