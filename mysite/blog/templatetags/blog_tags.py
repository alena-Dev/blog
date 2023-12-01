from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library() # используется для регистрации шаблонных тегов

@register.simple_tag
def total_posts(): # имя функции в качестве имени тега
    return Post.published.count() # число опубликованных постов

@register.inclusion_tag('blog/post/latest_posts.html') # словарь значений передается в latest_posts шаблон, к-й включается в шаблоне list
def show_latest_posts(count=9):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'lead_post': latest_posts[0],
            '1_3_posts': latest_posts[1:4],
            '1_2_posts': latest_posts[4:6],
            '2_3_post': latest_posts[7],
            'last_post': latest_posts[8]}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments') # общее число комментариев к посту
        ).order_by('-total_comments')[:count]

@register.filter(name='markdown') # имя фильтра
def markdown_format(text):
    return mark_safe(markdown.markdown(text)) # пометить результат как безопасный для избежания экранирования