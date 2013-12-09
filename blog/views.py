from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BlogPost

def index(request):
    latest_blog_posts = BlogPost.objects.order_by('-date')[:5]
    context = {'latest_blog_posts': latest_blog_posts}
    return render(request, 'blog/index.html', context)

@login_required
def new_post(request):
    pass

@login_required
def modify_post(request, id):
    pass

@login_required
def delete_post(request, id):
    pass

def view_post(request, id):
    pass
