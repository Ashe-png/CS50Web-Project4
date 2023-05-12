from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, null=True, related_name='liked_posts')
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post {self.id} posted by {self.author}'
    
class UserRelation(models.Model):
    userf = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.userf} is followed by {self.follower}'
    
    class Meta:
        unique_together = ('userf', 'follower')


