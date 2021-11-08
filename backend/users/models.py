from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings'
    )
