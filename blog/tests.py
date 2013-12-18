from django.test import TestCase
from .models import BlogPost, BlogComment
from .forms import BlogPostForm, CommentForm
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

    def test_new_post_get_view(self):
        UserFactory().create()
        self.client.login(username='user001', password='password123456')
        resp = self.client.get('/blog/new/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)

    def test_new_post_post_view(self):
        UserFactory().create()
        self.client.login(username='user001', password='password123456')
        self.client.post('/blog/new/', {'title': 'Title 001', 'text': 'Blog content example'})
        post = BlogPost.objects.all()[0]
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(post.title, 'Title 001')
        self.assertEqual(post.text, 'Blog content example')

    def test_add_comment_authenticated_view(self):
        blogpost = BlogPostFactory().create(True)
        UserFactory().create(username='user002')
        self.client.login(username='user002', password='password123456')
        url = '/blog/add_comment/%s/' % (str(blogpost.id))
        self.client.post(url, {'text': 'BlogPost comment'})
        comment = BlogComment.objects.all()[0]
        self.assertEqual(BlogComment.objects.count(), 1)
        self.assertEqual(comment.text, 'BlogPost comment')
        self.assertEqual(comment.user, 'user002')
        self.assertEqual(comment.post.id, blogpost.id)

    def test_add_comment_anonymous_view(self):
        blogpost = BlogPostFactory().create(True)
        url = '/blog/add_comment/%s/' % (str(blogpost.id))
        self.client.post(url, {'text': 'BlogPost comment'})
        comment = BlogComment.objects.all()[0]
        self.assertEqual(BlogComment.objects.count(), 1)
        self.assertEqual(comment.text, 'BlogPost comment')
        self.assertEqual(comment.user, 'Anonymous')
        self.assertEqual(comment.post.id, blogpost.id)

    def test_blogpost_form(self):
        user = UserFactory().create()
        blogpost_form = BlogPostForm({'title': 'Title 001', 'text': 'Blog content example'})
        blogpost_form.save(user, True)
        self.assertEqual(BlogPost.objects.count(), 1)

    def test_comment_form(self):
        post = BlogPostFactory().create(True)
        comment_form = CommentForm({'text': 'Comment from form'})
        comment_form.save(post.user, post, True)
        self.assertEqual(BlogComment.objects.count(), 1)

    def test_post_delete_view(self):
        blogpost = BlogPostFactory().create(True)
        CommentFactory().create(blogpost, "New comment - 1", True)
        CommentFactory().create(blogpost, "New comment - 2", True)
        self.client.login(username='user001', password='password123456')
        url = '/blog/%s/delete/' % (str(blogpost.id))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('message' in resp.context)
        self.assertEqual(resp.context['message'], 'Post deleted correctly.')
        self.assertEqual(BlogPost.objects.count(), 0)

    def test_post_delete_not_exist_view(self):
        UserFactory().create()
        self.client.login(username='user001', password='password123456')
        url = '/blog/%s/delete/' % (str(1))
        resp = self.client.get(url)
        self.assertTrue('message' in resp.context)
        self.assertEqual(resp.context['message'], 'Error: Post does not exist!')

    def test_post_delete_view_no_premission(self):
        blogpost = BlogPostFactory().create(True)
        CommentFactory().create(blogpost, "New comment - 1", True)
        CommentFactory().create(blogpost, "New comment - 2", True)
        UserFactory().create(username='user002')
        self.client.login(username='user002', password='password123456')
        url = '/blog/%s/delete/' % (str(blogpost.id))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('message' in resp.context)
        self.assertEqual(resp.context['message'], 'Error: you cannot delete this post!')
        self.assertEqual(BlogPost.objects.count(), 1)

    def test_post_modify_get_view(self):
        blogpost = BlogPostFactory().create(True)
        CommentFactory().create(blogpost, "New comment - 1", True)
        CommentFactory().create(blogpost, "New comment - 2", True)
        self.client.login(username='user001', password='password123456') # User is implicitly created by BlogPostFactory
        url = '/blog/%s/edit/' % (str(blogpost.id))
        resp = self.client.get(url)
        self.assertTrue('form' in resp.context)
        data = resp.context['form'].initial
        self.assertEqual(data['title'], 'Title Test')
        self.assertEqual(data['text'], 'Lorem ipsum tarapia tapioco...')

    def test_post_modify_post_view(self):
        blogpost = BlogPostFactory().create(True)
        CommentFactory().create(blogpost, "New comment - 1", True)
        CommentFactory().create(blogpost, "New comment - 2", True)
        self.client.login(username='user001', password='password123456') # User is implicitly created by BlogPostFactory
        url = '/blog/%s/edit/' % (str(blogpost.id))
        resp = self.client.get(url)
        self.assertTrue('form' in resp.context)
        data = resp.context['form'].initial
        data['text'] = 'New blog text'
        self.client.post(url, data)
        post = BlogPost.objects.all()[0]
        self.assertEqual(post.text, 'New blog text')
