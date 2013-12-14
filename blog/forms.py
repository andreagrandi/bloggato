from .models import BlogPost, Comment
from django.forms import ModelForm

class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('user',)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'user', 'date',)
