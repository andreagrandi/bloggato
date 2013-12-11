from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import BlogPost, Comment
from .forms import CommentForm

def index(request):
    posts = BlogPost.objects.order_by('-date')
    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}

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
    post = BlogPost.objects.get(id = int(id))
    comments = Comment.objects.filter(post = post)
    context = {'post': post, 'comments': comments, 'form': CommentForm()}
    return render(request, 'blog/post.html', context)

def add_comment(request, id):
    pass
