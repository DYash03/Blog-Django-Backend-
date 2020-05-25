from django.urls import path
from . import views
app_name = 'content'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog_list', views.blog_list, name='blog_list'),
    path('postComment', views.postComment, name='postComment'),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('Contact', views.Contactt, name='Contact'),
    path('<slug:slug>', views.blog_read, name='blog_read'),
    path('category/<str:category>', views.blog_category, name='blog_category'),
]
