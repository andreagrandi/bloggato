from django.test import TestCase
from .models import BlogPost, BlogComment
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
        comment = BlogComment()
        comment.post = blogpost
        comment.user = "Anonymous"
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
        blogpost_saved = BlogPost.objects.get(id = blogpost.id)
        self.assertEquals(blogpost_saved.title, blogpost.title, "BlogPost updated correctly")

    def test_post_delete(self):
        blogpost = BlogPostFactory().create(True)
        blogpost_id = blogpost.id
        blogpost.delete()
        blogpost_saved = BlogPost.objects.filter(id = blogpost_id)
        self.assertEqual(blogpost_saved.count(), 0, "BlogPost deleted correctly")

    def test_comment_create(self):
        blogpost = BlogPostFactory().create(True)
        comment = CommentFactory().create(blogpost, "New comment", True)
        self.assertTrue(comment.id > 0, "Comment created correctly")

    def test_comment_update(self):
        blogpost = BlogPostFactory().create(True)
        comment = CommentFactory().create(blogpost, "New comment", True)
        comment.text = "Modified comment"
        comment.save()
        comment_saved = BlogComment.objects.get(id = comment.id)
        self.assertEquals(comment_saved.text, comment.text, "Comment updated correctly")

    def test_comment_delete(self):
        blogpost = BlogPostFactory().create(True)
        comment = CommentFactory().create(blogpost, "New comment", True)
        comment_id = comment.id
        comment.delete()
        comment_saved = BlogComment.objects.filter(id = comment_id)
        self.assertEqual(comment_saved.count(), 0, "Comment deleted correctly")

    def test_post_view(self):
        blogpost = BlogPostFactory().create(True)
        CommentFactory().create(blogpost, "New comment - 1", True)
        CommentFactory().create(blogpost, "New comment - 2", True)
        url = '/blog/%s/' % (str(blogpost.id))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('post' in resp.context)
        self.assertTrue('comments' in resp.context)
        self.assertTrue('form' in resp.context)
        self.assertEqual(resp.context['post'].title, 'Title Test')
        self.assertEqual(resp.context['post'].text, 'Lorem ipsum tarapia tapioco...')
        self.assertEqual(resp.context['post'].user.username, 'user001')
        self.assertEqual(resp.context['comments'].count(), 2)
