from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Follow(models.Model):
    """Relationship between an authorized user and their following"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    idol = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentor')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'idol'],
                name='unique_follow'
                )
        ]
