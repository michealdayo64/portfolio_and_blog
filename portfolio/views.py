from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ProjectComment, ProjectViews
from blog.models import Category
#import redis
from django.conf import settings
import json
from django.http import JsonResponse
from django.utils import timesince


#r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
# Create your views here.

def port_index(request):
    proj = Project.objects.all()
    context = {
        'proj': proj
    }
    return render(request, 'portfolio_page/port_index.html', context)

def port_detail(request, id):
    proj_id = get_object_or_404(Project, id = id)
    all_comments = ProjectComment.objects.filter(post = proj_id)
    category_list = Category.objects.all()
    email = request.POST.get("email")
    comment = request.POST.get("comment")

    #total_views = r.incr('post:{}:views'.format(proj_id.id))
    total_views = 1
    view_id = ProjectViews.objects.filter(postview = proj_id)
    if view_id.exists():
        for i in view_id:
            i.views_count += 1
            i.save()
    else:
        ProjectViews.objects.create(postview = proj_id, views_count = total_views)

    view_count = ProjectViews.objects.get(postview = proj_id)
    if request.method == 'POST':

        comment_post = ProjectComment(email = email, comment = comment, post = proj_id)
        comment_post.save()
        return redirect("port-detail", proj_id.id)

    context = {
        'proj_id': proj_id,
        'all_comments': all_comments,
        'cat': category_list,
        'total_views': view_count.views_count
    }
    return render(request, 'portfolio_page/portfolio_detail.html', context)

def port_read_more(request, *args, **kwargs):
    print(kwargs.get('readmore'))
    upper = kwargs.get('readmore') #3
    lower = upper - 3 #0
    port_list = Project.objects.all()[lower:upper]
    #print(port_list.u)
    my_data = []
    for i in port_list:
        data = {
            'id': i.id,
            'title': i.title,
            'desc': i.description,
            'img': i.img.url,
            'user_like_count': i.user_like_proj.count(),
            'comment_count': i.project.count()
        }
        my_data.append(data)
    port_size = len(Project.objects.all())
    max_size = True if upper >= port_size else False
    
    return JsonResponse({'data': my_data, 'max_size': max_size, }, safe=False)


def port_comment(request, id):
    ns = json.loads(request.body)
    proj_id = get_object_or_404(Project, id = id)
    #all_comments = PostComment.objects.filter(post = blog_id).order_by('-date_publish')[:1]
    email = ns['email']
    comment = ns['comment']
    comment_id = None
    if request.method == 'POST':
        kk = ProjectComment.objects.create(email = email, comment = comment, post = proj_id)
        comment_id = kk.id
    uniq_comment = get_object_or_404(ProjectComment, id = comment_id)
    #print(timesince.timesince(uniq_comment.date_created))
    data = {
        'email': uniq_comment.email,
        'comment': uniq_comment.comment,
        'date': f'{timesince.timesince(uniq_comment.date_created)} Ago'
    }
    #comment_result.append(data)
    
    return JsonResponse(json.dumps(data), safe=False)

def port_like_unlike(request, id):
    post_id = Project.objects.get(id = id)
    #num_likes = post_id.user_like_post.count()
    user = request.user
    data = {}
    if user.is_authenticated:
        if not user in post_id.user_like_proj.all():
            post_id.user_like_proj.add(user)
            #return redirect("blog-id", post_id.id)
            print("Post Liked Successfully")
            data = {
                'result': "Project Liked Successfully",
                'num_likes': post_id.user_like_proj.count()
            }
            return JsonResponse(data=data, safe=False)
        else:
            post_id.user_like_proj.remove(user)
            #return redirect("blog-id", post_id.id)
            print("Post disliked Successfully")
            data = {
                'result': 'Project disliked Successfully',
                'num_likes': post_id.user_like_proj.count()
            }
            
            return JsonResponse(data=data, safe=False)
    #messages.warning(request, "User not authenticated")
    #return redirect("login")
    else:
        data = {
            'result': 'User not Authenticated'
        }
        return JsonResponse(data=data, safe=False)

def port_likeCount(request, id):
    post_id = Project.objects.get(id = id)
    data = {}
    if request.user.is_authenticated:
        p = post_id.user_like_proj.count()
        data = {
            'res': p
        }
        return JsonResponse(data=data, safe=False)
    else:
        p = post_id.user_like_proj.count()
        data = {
            'res': p
        }
        return JsonResponse(data = data, safe=False)


