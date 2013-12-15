from .models import BlogPost, BlogComment
from django.forms import ModelForm

class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('user',)

class CommentForm(ModelForm):
    class Meta:
        model = BlogComment
        exclude = ('post', 'user', 'date',)
