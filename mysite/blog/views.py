from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

'''Представление на основе класса для отображения списка постов

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'
'''

'''
Представление на основе функции для отображения списка постов
'''
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
                   'page_number': int(page_number)})

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

def post_share(request, post_id):
    # извлечь пост по id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST': # передать форму на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri( # ссылка на пост вставляется в письмо
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments:{cd['comments']}"
            send_mail(subject, message, 'alenakurakova59@gmail.com', [cd['to']])
            sent = True

    else: # отобразить пустую форму
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})