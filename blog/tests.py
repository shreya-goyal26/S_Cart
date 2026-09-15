from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import BlogPost, BlogComment

class BlogSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username="editor_arjun",
            email="arjun@blog.com",
            password="password123",
            first_name="Arjun",
            last_name="Sharma"
        )
        self.post = BlogPost.objects.create(
            author_user=self.author,
            title="The 2025 Guide to E-Commerce Trends",
            slug="the-2025-guide-to-ecommerce-trends",
            author="Arjun Sharma",
            category="Technology",
            tags="Tech, Trends, Shopping",
            read_time="6 min read",
            excerpt="An in-depth look at emerging retail technologies.",
            content="Full article content describing next-gen e-commerce.",
            views=10
        )

    def test_blog_home_loads_posts(self):
        response = self.client.get(reverse('BlogHome'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The 2025 Guide to E-Commerce Trends")

    def test_post_detail_increments_views(self):
        initial_views = self.post.views
        response = self.client.get(reverse('BlogPostDetail', args=[self.post.post_id]))
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_views + 1)

    def test_add_blog_comment(self):
        response = self.client.post(reverse('BlogAddComment', args=[self.post.post_id]), {
            'name': 'Curious Reader',
            'email': 'reader@domain.com',
            'comment': 'Brilliant insights on future checkout flows!'
        })
        self.assertEqual(BlogComment.objects.filter(post=self.post).count(), 1)
        comment = BlogComment.objects.first()
        self.assertEqual(comment.name, 'Curious Reader')

    def test_create_blog_post_authenticated(self):
        self.client.login(username='editor_arjun', password='password123')
        response = self.client.post(reverse('BlogCreatePost'), {
            'title': 'Minimalist Desk Setups for Creators',
            'category': 'Lifestyle',
            'tags': 'Workspace, Design',
            'read_time': '4 min read',
            'excerpt': 'Elevate your workspace with these essentials.',
            'content': 'Paragraphs about desk ergonomics.'
        })
        self.assertEqual(BlogPost.objects.count(), 2)
        new_post = BlogPost.objects.get(title='Minimalist Desk Setups for Creators')
        self.assertEqual(new_post.author_user, self.author)
