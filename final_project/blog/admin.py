from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment, Post_category, Tag, User, Like, Dislike
from .forms import UserForm, Post_form, TagForm, Post_Category_Form


class CustomUserAdmin(UserAdmin):
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


class PostAdmin(admin.ModelAdmin):
    form = Post_form
    model = Post
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'image', 'category', 'author', 'post_date')
        }),
    )


class TagAdmin(admin.ModelAdmin):
    form = TagForm
    model = Tag
    fieldsets = (
        (None, {
            'fields': ('name', 'post')
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fieldsets = (
        (None, {
            'fields': ('content', 'author', 'comment_date')
        }),
    )


class Post_categoryAdmin(admin.ModelAdmin):
    form = Post_Category_Form
    model = Post_category
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


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post_category, Post_categoryAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)

