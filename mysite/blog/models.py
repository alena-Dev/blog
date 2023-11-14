from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):

    class Status(models.TextChoices): 
        DRAFT = 'DF', 'Daft' # черновик поста
        PUBLISHED = 'PB', 'Published' # варианты статуса, пары "значение-метка"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250) # короткая метка
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

    class Meta: # метаданные модели
        ordering = ['-publish'] # если в запросе не указан порядок сортировки постов, задается обратный порядок (сначала новые) по полю publish
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self) -> str:
        return self.title
