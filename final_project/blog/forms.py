from django import forms
from django.forms import ModelForm, Textarea
from .models import Tag, Post_category, Post, User, Comment
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import NumberInput
from dal import autocomplete
from image_cropping import ImageCropWidget


REQUIRED_MSG = 'این که خالیه عامو!!'


class Post_form(ModelForm):
    class Meta:
        model = Post
        fields = ['post_date', 'title', 'text', 'image', 'category']
        widgets = {
            'tag': autocomplete.ModelSelect2Multiple(url='blog:Tag-autocomplete')
        }
        labels = {
            'title': _('عنوان پست'),
            'text': _('متن پست'),
            'image': _('تصویر مرتبط'),
            'post_date': _('تاریخ انتشار'),
            'category': _('دسته بندی'),
        }
        error_messages = {
            'title': {
                'max_lenght': _('این عنوان برای پست بسیار طولانی است'),
            },
            'text': {
                'max_lenght': _('این متن برای پست بسیار طولانی است'),
            }
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'post']
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 2, 'placeholder': "نظر شما..."}),
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
        fields = ['name']
        labels = {
            'name': _('عنوان دسته بندی'),
        }


class UserForm(ModelForm):
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(), )
    ConfirmPassword = forms.CharField(label='تایید رمز عبور', widget=forms.PasswordInput(), )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'birthdate', 'email', 'profile_image', 'password'
                  ,'ConfirmPassword']
        widgets = {
            'birthdate': NumberInput(attrs={'type': 'date'}),
            'profile_image': ImageCropWidget(),
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'birthdate': _('تاریخ تولد'),
            'email': _('آدرس ایمیل'),
            'profile_image': _('عکس پروفایل'),
            'password': _('رمز عبور'),
            'ConfirmPassword': _('تایید رمز عبور'),
            'username': _('نام کاربری'),

        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = user.set_password(self.cleaned_data["password"])
        confirmpassword = user.set_password(self.cleaned_data["password"])
        if password and confirmpassword and password == confirmpassword:
            user.save()
        return user
