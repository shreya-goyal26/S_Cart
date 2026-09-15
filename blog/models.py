from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    author_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.CharField(max_length=100, default="S_Cart Editorial")
    author_role = models.CharField(max_length=100, default="Senior Tech & Lifestyle Editor", blank=True)
    author_avatar = models.CharField(max_length=10, default="A")
    category = models.CharField(max_length=100, default="Technology")
    tags = models.CharField(max_length=200, default="Tech, Shopping")
    read_time = models.CharField(max_length=50, default="5 min")
    excerpt = models.TextField(default="")
    content = models.TextField(default="")
    thumbnail = models.ImageField(upload_to="blog/images", default="", blank=True)
    thumbnail_url = models.CharField(max_length=500, default="", blank=True)
    icon = models.CharField(max_length=10, default="📱")
    is_featured = models.BooleanField(default=False)
    pub_date = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(post_id=self.post_id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def display_thumbnail(self):
        if self.thumbnail:
            try:
                return self.thumbnail.url
            except Exception:
                pass
        if self.thumbnail_url:
            return self.thumbnail_url
        return ""

    @property
    def get_tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class BlogComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
