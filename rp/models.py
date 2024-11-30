from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='blog_posts',
                             verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                               related_name='posts',
                               null=True, blank=True,
                               verbose_name='Категория')
    content = models.TextField(verbose_name='Содержание')
    media = models.ImageField(upload_to='blog/%Y/%m/%d/', 
                            blank=True, null=True,
                            verbose_name='Изображение')
    video = models.FileField(upload_to='videos/%Y/%m/%d/', 
                            blank=True, null=True, 
                            verbose_name='Видео')
    publish = models.DateTimeField(default=timezone.now,
                                 verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True,
                                 verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True,
                                 verbose_name='Обновлено')
    status = models.CharField(max_length=10, 
                            choices=STATUS_CHOICES,
                            default='draft',
                            verbose_name='Статус')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='Дизлайки')

    
    class  Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-list')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name='Родительский комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments', verbose_name='Автор')
    content = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    active = models.BooleanField(default=True, verbose_name='Активный')
    image = models.ImageField(upload_to='comments/%Y/%m/%d/', blank=True, null=True, verbose_name='Изображение')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='Дизлайки')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Vote(models.Model):
    VOTE_CHOICES = (
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes', verbose_name='Пост')
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES, verbose_name='Голос')

    class Meta:
        unique_together = ('user', 'post')

class CommentVote(models.Model):
    VOTE_CHOICES = (
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_votes', verbose_name='Пользователь')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes', verbose_name='Комментарий')
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES, verbose_name='Голос')

    class Meta:
        unique_together = ('user', 'comment')
