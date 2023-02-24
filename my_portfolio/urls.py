"""my_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
#from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from blog.views import index, blog_list, blog_detail, post_comment, like_unlike_post, likeCount, searchBlog
from portfolio.views import port_index, port_detail, port_read_more, port_comment, port_like_unlike, port_likeCount
from account.views import register, login_page, logout_page, activate, resetPassword
from contact.views import contact_message
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('blog-index/', blog_list, name='blog-index'),
    re_path(r'^download/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path('blog-id/<id>/', blog_detail, name='blog-id'),
    path('post-comment/<id>/', csrf_exempt(post_comment), name='post-comment'),
    path('port-index/', port_index, name='port-index'),
    path('port-detail/<id>/', port_detail, name='port-detail'),
    path('read-more/<int:readmore>/', port_read_more, name='read-more'),
    #path('contact_page/', contact, name='contact_page'),
    path('register/', register, name='register'),
    path('login/', login_page, name = 'login'),
    path('logout/', logout_page, name = 'logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('reset-password/', resetPassword, name = 'reset-password'), 
    path('like_unlike/<id>/', csrf_exempt(like_unlike_post), name = 'like_unlike'),
    path('like_count/<id>/', likeCount, name = 'like_count'),
    path('port-comment/<id>/', csrf_exempt(port_comment), name = 'port-comment'),
    path('port_like_unlike/<id>/', csrf_exempt(port_like_unlike), name = 'port_like_unlike'),
    path('port_like_count/<id>/', port_likeCount, name = 'port_like_count'),
    path('contact-page/', contact_message, name = 'contact-page'),
    path('search-block/', csrf_exempt(searchBlog), name = 'search-blog'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
