from .models import BlogPost
from django import forms

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('user',)
