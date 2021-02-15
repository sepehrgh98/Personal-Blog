from django.contrib import admin
from .models import Post, Post_state, Comment, Post_category, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Post_state)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Post_category)

