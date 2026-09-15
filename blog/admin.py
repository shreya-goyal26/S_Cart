from django.contrib import admin
from .models import BlogPost, BlogComment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'pub_date', 'views', 'is_featured')
    list_filter = ('category', 'is_featured', 'pub_date')
    search_fields = ('title', 'content', 'tags', 'author')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'created_at')
    search_fields = ('name', 'email', 'comment')
