from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', # использовать дату публикации и слаг для URL-адреса
         views.post_detail, 
         name='post_detail')
]
