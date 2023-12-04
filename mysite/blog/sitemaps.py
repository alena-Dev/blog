from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly' # указывает частоту изменения страниц постов
    priority = 0.9 # релевантность страниц постов на веб-сайте

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated