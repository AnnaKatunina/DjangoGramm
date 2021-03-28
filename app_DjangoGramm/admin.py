from django.contrib import admin

from app_DjangoGramm.models import User, Profile, Post, Follower

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follower)
