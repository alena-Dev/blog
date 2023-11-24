from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html',
                  {'posts': posts,
                   'latest_post': posts.latest('id')})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'other_posts': Post.objects.all()[:3]}) # returns the first 3 objects