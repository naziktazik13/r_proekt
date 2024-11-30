from django.contrib import admin
from .models import Category, Post, Comment, Profile, Vote, CommentVote
# Register your models here.

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Vote)
admin.site.register(CommentVote)