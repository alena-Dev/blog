from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                            .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices): 
        DRAFT = 'DF', 'Daft' # черновик поста
        PUBLISHED = 'PB', 'Published' # варианты статуса, пары "значение-метка"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, # короткая метка
                            unique_for_date='publish') # поле slug должно быть уникальным для даты, сохраненной в поле publish, чтобы избежать дублирование записей

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, # при удалении пользователя удалятся все его посты
                               related_name='blog_posts') # для обращения к объектам из объекта User, используя обозначение user.blog_posts
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) # дата будет обновляться автоматически
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager() # manager by default
    published = PublishedManager() # the new one

    tags = TaggableManager() # менеджер, к-й позволяет добавлять, извлекать и удалять теги из объектов Post

    class Meta: # метаданные модели
        ordering = ['-publish'] # если в запросе не указан порядок сортировки постов, задается обратный порядок (сначала новые) по полю publish
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self): # формирует URL-адрес динамически
        return reverse("blog:post_detail", args=[self.publish.year, # позиционный аргумент
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, # пост, к к-му написан комментарий, можно извлекать с помощью comment.post
                             on_delete=models.CASCADE,
                             related_name='comments') # для обращения к комментариям из объектов Post с помощью post.comments.all()
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True) # дата при создании объекта
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # по умолчанию все комментарии активны, удалять комментари можно с сайта администрирования

    class Meta:
        ordering = ['-created'] # сортировать в хронологическом порядке
        indexes = [
            models.Index(fields=['-created']), # индексировать в возрастающем порядке
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'