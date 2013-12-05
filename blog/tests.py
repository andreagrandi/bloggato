from django.test import TestCase
from .models import BlogPost
from django.contrib.auth.models import User

class BlogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = "user001", email = "email@domain.com", password = "password123456")

    def test_post_creation(self):
        blogpost = BlogPost()
        blogpost.user = self.user
        blogpost.title = "Title Test"
        blogpost.text = "Lorem ipsum tarapia tapioco..."
        blogpost.save()
        self.assertTrue(blogpost.id > 0, "BlogPost created correctly")

    def test_post_update(self):
        blogpost = BlogPost()
        blogpost.user = self.user
        blogpost.title = "Title Test"
        blogpost.text = "Lorem ipsum tarapia tapioco..."
        blogpost.save()
        self.assertTrue(blogpost.id > 0, "BlogPost created correctly")
        blogpost.title = "Title Test - modified"
        blogpost.save()
        blogpost_id = blogpost.id
        blogpost_saved = BlogPost.objects.get(id = blogpost_id)
        self.assertEquals(blogpost_saved.title, blogpost.title, "BlogPost updated correctly")

    def test_post_delete(self):
        blogpost = BlogPost()
        blogpost.user = self.user
        blogpost.title = "Title Test"
        blogpost.text = "Lorem ipsum tarapia tapioco..."
        blogpost.save()
        blogpost_id = blogpost.id
        blogpost.delete()
        blogpost_saved = BlogPost.objects.filter(id = blogpost_id)
        self.assertEqual(blogpost_saved.count(), 0, "BlogPost deleted correctly")
