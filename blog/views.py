from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, world. You're at the Bloggato index.")

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
