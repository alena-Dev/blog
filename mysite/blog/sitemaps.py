from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly' # указывает частоту изменения страниц постов
    priority = 0.9 # релевантность страниц постов на веб-сайте

    # url-адрес каждого объекта Post формируется путем вызова его метода get_absolute_url()

    def items(self): # подлежит включению в эту карту сайта
        return Post.published.all()
    
    def lastmod(self, obj): # получает каждый объект из items() и возвращает время последнего изменения объекта
        return obj.updated