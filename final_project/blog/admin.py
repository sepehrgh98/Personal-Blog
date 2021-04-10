from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment, Category, Tag, User, Like, Dislike
from .forms import UserForm, Post_form, TagForm, Category_Form
from image_cropping import ImageCroppingMixin
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group

class CustomUserAdmin(ImageCroppingMixin, UserAdmin):
    form = UserForm
    model = User
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'birthdate', 'email', 'profile_image',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class TagAdmin(admin.ModelAdmin):
    form = TagForm
    model = Tag
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    form = Category_Form
    model = Category
    fieldsets = (
        (None, {
            'fields': ('name', 'parent_category')
        }),
    )


class LikeAdmin(admin.ModelAdmin):
    model = Like
    fieldsets = (
        (None, {
            'fields': ('user', 'state_date', 'post')
        }),
    )


class DislikeAdmin(admin.ModelAdmin):
    model = Dislike
    fieldsets = (
        (None, {
            'fields': ('user', 'state_date', 'post')
        }),
    )


class likeInline(admin.TabularInline):
    model = Like


class dislikeInline(admin.TabularInline):
    model = Dislike


class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(ImageCroppingMixin, admin.ModelAdmin):
    form = Post_form
    model = Post
    inlines = [
        likeInline,
        dislikeInline,
        CommentInline,
    ]
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'image', 'category', 'author', 'post_date', 'cropping')
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fieldsets = (
        (None, {
            'fields': ('text', 'author', 'comment_date', 'post')
        }),
    )

User = get_user_model()


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(),
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
