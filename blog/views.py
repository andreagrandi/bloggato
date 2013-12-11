from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import BlogPost

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
    pass
