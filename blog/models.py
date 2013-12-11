from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length = 120)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(BlogPost)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.text[:60]))
