from django.contrib import admin
from .models import Post, Post_state, Comment, Post_content, Post_category

# Register your models here.
admin.site.register(Post)
admin.site.register(Post_state)
admin.site.register(Comment)
admin.site.register(Post_content)
admin.site.register(Post_category)

