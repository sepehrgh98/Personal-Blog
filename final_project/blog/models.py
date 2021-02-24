from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    birthdate = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=500)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


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
