from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    post_list = Post.published.all()

    paginator = Paginator(post_list, 5) # отображать по 5 поста на страницу
    page_number = request.GET.get('page', 1) # GET-параметр page содержит запрошенный номер страницы. Если его нет, загрузить первую страницу результатов
    try:
        posts = paginator.page(page_number) # передаем номер страницы и объект posts в шаблон
    except PageNotAnInteger:
        posts = paginator.page(1) # Если запрошенная страница не является целым числом, вернуть первую страницу результатов
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # Если запрошенная страница находится вне диапазона, вернуть последнюю страницу результатов

    return render(request, 'blog/post/list.html',
                  {'posts': posts, # 'Page' object
                   'latest_post': post_list.latest('id'),
                   'page_number': page_number})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'list_posts': Post.objects.exclude(id=post.id).all()[:3]}) # returns the first 3 objects