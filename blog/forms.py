from .models import BlogPost, BlogComment
from django.forms import ModelForm

class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('user',)

    def save(self, user, commit=True):
        post = super(BlogPostForm, self).save(commit=False)
        post.user = user

        if commit:
            post.save()
        return post

class CommentForm(ModelForm):
    class Meta:
        model = BlogComment
        exclude = ('post', 'user',)

    def save(self, user, post, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.user = user
        comment.post = post

        if commit:
            comment.save()
        return comment
