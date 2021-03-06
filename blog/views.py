from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import BlogPost, BlogComment
from .forms import CommentForm, BlogPostForm

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
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(user = request.user)
            return HttpResponseRedirect('/blog/%d/' % post.id)

    form = BlogPostForm()
    context = {'form': form}
    return render(request, 'blog/new_post.html', context)

@login_required
def modify_post(request, id):
    if id:
        post = get_object_or_404(BlogPost, pk=id)
        if post.user != request.user:
            context = {'message': 'You are not allowed to modify this post.'}
            return render(request, 'error.html', context)

    if request.POST:
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(user = request.user)
            comments = BlogComment.objects.filter(post = post)
            context = {'post': post, 'comments': comments, 'form': CommentForm()}
            return render(request, 'blog/post.html', context)
    else:
        form = BlogPostForm(instance=post)
        context = {'form': form, 'post': post}
        return render(request, 'blog/modify_post.html', context)

@login_required
def delete_post(request, id):
    try:
        post = BlogPost.objects.get(id=id)
    except BlogPost.DoesNotExist:
        context = {'message': 'Error: Post does not exist!', 'success': 'false'}
        return render(request, 'blog/post_deleted.html', context)

    if request.user == post.user or request.user.is_superuser:
        comments = BlogComment.objects.filter(post=id)
        
        for c in comments:
            c.delete()

        post.delete()

        context = {'message': 'Post deleted correctly.', 'success': 'true'}
        return render(request, 'blog/post_deleted.html', context)
    else:
        context = {'message': 'Error: you cannot delete this post!', 'success': 'false'}
        return render(request, 'blog/post_deleted.html', context)

def view_post(request, id):
    post = BlogPost.objects.get(id = int(id))
    comments = BlogComment.objects.filter(post = post)
    context = {'post': post, 'comments': comments, 'form': CommentForm()}
    return render(request, 'blog/post.html', context)

def add_comment(request, id):
    form = CommentForm(request.POST)
    
    if form.is_valid():
        post = BlogPost.objects.get(id=id)

        if request.user.is_authenticated():
            user = request.user.username
        else:
            user = "Anonymous"

        form.save(user = user, post = post)

        return HttpResponseRedirect('/blog/%d/' % post.id)

def about(request):
    return render(request, 'blog/about.html')

