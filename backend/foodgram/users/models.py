from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    email = models.EmailField('Email', max_length=254, unique=True)
    username = models.CharField('Username', max_length=150, unique=True)
    first_name = models.CharField('Name', max_length=150)
    last_name = models.CharField('Surname', max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецептов',
        related_name='subscribing',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='subscribers',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписку'
        verbose_name_plural = 'Подписки'
        ordering = ['author', 'user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_author_user_subscribing'
            )
        ]

    def __str__(self):
        return f'Подписка {self.user.username} на {self.author.username}'

    def get_absolute_url(self):
        return reverse('subscriptions')
