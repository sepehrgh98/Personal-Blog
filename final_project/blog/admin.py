from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Post_state, Comment, Post_category, Tag, User

# Register your models here.
admin.site.register(Post)
admin.site.register(Post_state)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Post_category)
admin.site.register(User , UserAdmin)
