from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', db_index=True, max_length=150, unique=True,
        error_messages={'required': 'Поле должно быть заполнено',
                        'unique': ('Пользователь с таким '
                                   'username уже зарегестрирован')},
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    email = models.EmailField(
        'Электронная почта',
        error_messages={'required': 'Поле должно быть заполнено',
                        'unique': ('Пользователь с таким '
                                   'емейлом уже зарегестрирован')},
        db_index=True, unique=True, max_length=254)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.get_full_name()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='restrict_manyfollow',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='self_following_check',
            )
        ]
