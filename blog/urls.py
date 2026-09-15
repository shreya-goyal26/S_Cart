from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="BlogHome"),
    path("post/<int:myid>/", views.post_detail, name="BlogPostDetail"),
    path("article/<slug:slug>/", views.post_detail_slug, name="BlogPostDetailSlug"),
    path("post/<int:myid>/comment/", views.add_comment, name="BlogAddComment"),
    path("create/", views.create_post, name="BlogCreatePost"),
    path("edit/<int:myid>/", views.edit_post, name="BlogEditPost"),
    path("delete/<int:myid>/", views.delete_post, name="BlogDeletePost"),
]