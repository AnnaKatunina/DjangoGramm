from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return f'{self.username} {self.email}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default_avatar.png')

    def __str__(self):
        return f'{self.full_name}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    description = models.TextField(blank=True)
    published_at = models.DateField(auto_now_add=True)


class Follower(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    @classmethod
    def follow(cls, current_user, new_following):
        following, created = cls.objects.get_or_create(
            user_id=current_user,
            following_user_id=new_following
        )

    @classmethod
    def unfollow(cls, current_user, no_following):
        following = cls.objects.filter(
            user_id=current_user,
            following_user_id=no_following
        ).delete()

    def __str__(self):
        return f'{self.user_id} follows {self.following_user_id}'
