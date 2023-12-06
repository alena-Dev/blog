from django.db.models.base import Model
import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed): # новостная лента
    title = 'My blog'
    link = reverse_lazy('blog:post_list') # функция-утилита используется для того, чтобы генерировать url-адрес для атрибута link
    description = 'New posts of my blog'

    def items(self): # извлекает включаемые в новостную ленту объекты
        return Post.published.all()[:5]
    
    def item_title(self, item): # возвращает заголовок
        return item.title
    
    def item_description(self, item: Model) -> str: # возвращает описание
        return truncatewords_html(markdown.markdown(item.body), 30) # сокращает описание поста до 30 слов
    
    def item_pubdate(self, item): # возвращает дату публикации
        return item.publish