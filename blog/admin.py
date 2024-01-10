from django.contrib import admin
from .models import Comment, Post
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ("status", "date_posted", "category")
    list_display = ("title", "slug", "author", "date_posted", "status", "category")
    search_fields = ['title', 'content']
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ("author", "content", "post", "date_posted", "updated_on", "approved")
    list_filter = ("approved", "date_posted", "updated_on")
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)