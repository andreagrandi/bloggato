from django.test import TestCase
from .models import BlogPost, Comment
from django.contrib.auth.models import User

class UserFactory(object):
    def create(self, username="user001", email="email@domain.com", password="password123456"):
        user = User.objects.create_user(username = username, email = email, password = password)
        return user

class BlogPostFactory(object):
    def create(self, save=False):
        blogpost = BlogPost()
        blogpost.user = UserFactory().create()
        blogpost.title = "Title Test"
        blogpost.text = "Lorem ipsum tarapia tapioco..."

        if save==True:
            blogpost.save()

        return blogpost

class CommentFactory(object):
    def create(self, blogpost, text="Test comment", save=False):
        comment = Comment()
        comment.post = blogpost
        comment.user = UserFactory().create("user002", "email002@domain.com", "password123456")
        comment.text = text

        if save==True:
            comment.save()

        return comment

class BlogTest(TestCase):
    def setUp(self):
        pass

    def test_post_creation(self):
        blogpost = BlogPostFactory().create(True)
        self.assertTrue(blogpost.id > 0, "BlogPost created correctly")

    def test_post_update(self):
        blogpost = BlogPostFactory().create(True)
        self.assertTrue(blogpost.id > 0, "BlogPost created correctly")
        blogpost.title = "Title Test - modified"
        blogpost.save()
        blogpost_id = blogpost.id
        blogpost_saved = BlogPost.objects.get(id = blogpost_id)
        self.assertEquals(blogpost_saved.title, blogpost.title, "BlogPost updated correctly")

    def test_post_delete(self):
        blogpost = BlogPostFactory().create(True)
        blogpost_id = blogpost.id
        blogpost.delete()
        blogpost_saved = BlogPost.objects.filter(id = blogpost_id)
        self.assertEqual(blogpost_saved.count(), 0, "BlogPost deleted correctly")
