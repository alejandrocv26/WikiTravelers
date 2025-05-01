from django.contrib import admin
from .models import Country, Post, Comment, Profile

admin.site.register(Country)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
