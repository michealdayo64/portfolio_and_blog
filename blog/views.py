from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import redis
from django.utils import timesince
from .models import Post, Category, PostComment, PostViews
from portfolio.models import Project
from django.conf import settings
import json
import os
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


'''from .tasks import test_func
def test(request):
    test_func.delay()
    return HttpResponse("Done")'''

#r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def index(request):
    posts = Post.objects.all().order_by('-date_publish')[:3]
    recent_proj = Project.objects.all().order_by('-date_created')[:3]
    context = {
        'posts': posts,
        'recent_proj': recent_proj
    }
    return render(request, 'home_page/index.html', context)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/file_upload")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
    raise Http404

def blog_list(request):
    posts = Post.objects.filter(is_posted = True).order_by('-date_publish')
    category_list = Category.objects.all()


    paginator = Paginator(posts, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_query = paginator.page(page)
    except PageNotAnInteger:
        paginated_query = paginator.page(1)
    except EmptyPage:   
        paginated_query = paginator.page(paginator.num_pages) 
    context = {
        'posts': paginated_query,
        'page_request_var': page_request_var,
        'cat': category_list
    }
    return render(request, "blog_page/blog_index.html", context)

def blog_detail(request, id):
    blog_id = get_object_or_404(Post, id = id)
    num_likes = blog_id.user_like_post.count()
    all_comments = PostComment.objects.filter(post = blog_id).order_by('-date_created')
    category_list = Category.objects.all()
    email = request.POST.get("email")
    comment = request.POST.get("comment")

    #total_views = r.incr('post:{}:views'.format(blog_id.id))
    total_views = 1
    view_id = PostViews.objects.filter(postview = blog_id)
    if view_id.exists():
        for i in view_id:
            i.views_count += 1
            i.save()
    else:
        PostViews.objects.create(postview = blog_id, views_count = total_views)

    view_count = PostViews.objects.get(postview = blog_id)
    if request.method == 'POST':

        comment_post = PostComment(email = email, comment = comment, post = blog_id)
        comment_post.save()
        return redirect("blog-id", blog_id.id)

    
    context = {
        'post_id': blog_id,
        #'num_likes': num_likes,
        'all_comments': all_comments,
        'cat': category_list,
        'total_views': view_count.views_count
    }
    return render(request, 'blog_page/blog_detail.html', context)


def post_comment(request, id):
    ns = json.loads(request.body)
    blog_id = get_object_or_404(Post, id = id)
    #all_comments = PostComment.objects.filter(post = blog_id).order_by('-date_publish')[:1]
    email = ns['email']
    comment = ns['comment']
    comment_id = None
    if request.method == 'POST':
        kk = PostComment.objects.create(email = email, comment = comment, post = blog_id)
        comment_id = kk.id
    uniq_comment = get_object_or_404(PostComment, id = comment_id)
    #print(timesince.timesince(uniq_comment.date_created))
    data = {
        'email': uniq_comment.email,
        'comment': uniq_comment.comment,
        'date': f'{timesince.timesince(uniq_comment.date_created)} Ago'
    }
    #comment_result.append(data)
    
    return JsonResponse(json.dumps(data), safe=False)

def newsLetter(request):
    pass


def like_unlike_post(request, id):
    post_id = Post.objects.get(id = id)
    #num_likes = post_id.user_like_post.count()
    user = request.user
    data = {}
    if user.is_authenticated:
        if not user in post_id.user_like_post.all():
            post_id.user_like_post.add(user)
            #return redirect("blog-id", post_id.id)
            print("Post Liked Successfully")
            data = {
                'result': "Post Liked Successfully",
                'num_likes': post_id.user_like_post.count()
            }
            return JsonResponse(data=data, safe=False)
        else:
            post_id.user_like_post.remove(user)
            #return redirect("blog-id", post_id.id)
            print("Post disliked Successfully")
            data = {
                'result': 'Post disliked Successfully',
                'num_likes': post_id.user_like_post.count()
            }
            
            return JsonResponse(data=data, safe=False)
    #messages.warning(request, "User not authenticated")
    #return redirect("login")
    else:
        data = {
            'result': 'User not Authenticated'
        }
        return JsonResponse(data=data, safe=False)

def likeCount(request, id):
    post_id = Post.objects.get(id = id)
    data = {}
    if request.user.is_authenticated:
        p = post_id.user_like_post.count()
        data = {
            'res': p
        }
        return JsonResponse(data=data, safe=False)
    else:
        p = post_id.user_like_post.count()
        data = {
            'res': p
        }
        return JsonResponse(data = data, safe=False)

    
    



