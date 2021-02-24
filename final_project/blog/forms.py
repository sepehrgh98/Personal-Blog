from django import forms
from django.forms import ModelForm
from .models import Tag, Post_category, Post, User
from django.utils.translation import gettext_lazy as _

REQUIRED_MSG = 'این که خالیه عامو!!'


class Post_form(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'post_date', 'title', 'text', 'image']
        labels = {
            'title': _('عنوان پست'),
            'text': _('متن پست'),
            'image': _('تصویر مرتبط')
        }
        help_texts = {
            'title': _('عنوان پست مورد نظر را در این کادر قرار دهید'),
            'text': _('متن مورد نظر را در این کادر بنویسید'),
            'image': _('تصویر مرتبط با پست را اینجا پیوست دهید')
        }
        error_messages = {
            'title': {
                'max_lenght': _('این عنوان برای پست بسیار طولانی است'),
            },
            'text': {
                'max_lenght': _('این متن برای پست بسیار طولانی است'),
            }
        }


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': _('عنوان برچسب'),
        }


class Post_Category_Form(ModelForm):
    class Meta:
        model = Post_category
        fields = ['name', 'super_category']
        labels = {
            'name': _('عنوان دسته بندی'),
            'super_category': _('زیر دسته'),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthdate', 'email', 'profile_image']
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'birthdate': _('تاریخ تولد'),
            'email': _('آدرس ایمیل'),
            'profile_image': _('عکس پروفایل'),
        }
