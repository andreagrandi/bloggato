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
