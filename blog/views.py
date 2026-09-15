from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F, Count
from .models import BlogPost, BlogComment


def index(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    tag = request.GET.get('tag', '').strip()

    posts = BlogPost.objects.all().order_by('-pub_date')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__icontains=query) |
            Q(category__icontains=query) |
            Q(author__icontains=query)
        )

    if category and category.lower() != 'all':
        posts = posts.filter(category__iexact=category)

    if tag:
        posts = posts.filter(tags__icontains=tag)

    featured_post = BlogPost.objects.filter(is_featured=True).first()
    if not featured_post:
        featured_post = posts.first()

    popular_posts = BlogPost.objects.all().order_by('-views')[:5]
    all_categories = BlogPost.objects.values('category').annotate(count=Count('post_id')).order_by('-count')

    # Collect unique tags
    all_tags_raw = BlogPost.objects.values_list('tags', flat=True)
    all_tags = set()
    for t_str in all_tags_raw:
        if t_str:
            for item in t_str.split(','):
                if item.strip():
                    all_tags.add(item.strip())

    total_articles = BlogPost.objects.count()
    total_comments = BlogComment.objects.count()

    context = {
        'posts': posts,
        'featured_post': featured_post,
        'popular_posts': popular_posts,
        'all_categories': all_categories,
        'all_tags': sorted(list(all_tags))[:15],
        'query': query,
        'active_category': category or 'All',
        'active_tag': tag,
        'stats': {
            'articles': total_articles,
            'comments': total_comments,
        }
    }
    return render(request, "blog/index.html", context)


def post_detail(request, myid):
    post = get_object_or_404(BlogPost, post_id=myid)

    # Increment view counter
    BlogPost.objects.filter(post_id=post.post_id).update(views=F('views') + 1)
    post.refresh_from_db(fields=['views'])

    comments = post.comments.all().order_by('-created_at')
    related_posts = BlogPost.objects.filter(category=post.category).exclude(post_id=post.post_id)[:3]
    popular_posts = BlogPost.objects.all().order_by('-views')[:4]
    all_categories = BlogPost.objects.values('category').annotate(count=Count('post_id')).order_by('-count')

    context = {
        'post': post,
        'comments': comments,
        'comment_count': comments.count(),
        'related_posts': related_posts,
        'popular_posts': popular_posts,
        'all_categories': all_categories,
    }
    return render(request, "blog/post_detail.html", context)


def post_detail_slug(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return post_detail(request, post.post_id)


def add_comment(request, myid):
    post = get_object_or_404(BlogPost, post_id=myid)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        comment_text = request.POST.get('comment', '').strip()

        if request.user.is_authenticated and not name:
            name = request.user.get_full_name() or request.user.username
        if request.user.is_authenticated and not email:
            email = request.user.email

        if not name:
            name = "Guest Reader"

        if comment_text:
            user = request.user if request.user.is_authenticated else None
            comment = BlogComment.objects.create(
                post=post,
                user=user,
                name=name,
                email=email,
                comment=comment_text
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Your comment has been posted!',
                    'comment': {
                        'name': comment.name,
                        'text': comment.comment,
                        'date': comment.created_at.strftime('%b %d, %Y'),
                        'avatar': comment.name[0].upper() if comment.name else 'G'
                    }
                })
            messages.success(request, "Your comment has been posted!")
            return redirect('BlogPostDetail', myid=post.post_id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please write a comment.'}, status=400)
            messages.error(request, "Please write a comment.")

    return redirect('BlogPostDetail', myid=post.post_id)


@login_required(login_url='ShopLogin')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', 'Technology').strip()
        tags = request.POST.get('tags', '').strip()
        read_time = request.POST.get('read_time', '5 min').strip()
        excerpt = request.POST.get('excerpt', '').strip()
        content = request.POST.get('content', '').strip()
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        icon = request.POST.get('icon', '📝').strip()

        if not title or not content:
            messages.error(request, "Please provide at least a title and content for your article.")
            return render(request, "blog/create_post.html")

        if not excerpt:
            excerpt = content[:180] + "..." if len(content) > 180 else content

        author_name = request.user.get_full_name() or request.user.username
        post = BlogPost(
            author_user=request.user,
            title=title,
            author=author_name,
            author_role="Contributor",
            author_avatar=author_name[0].upper(),
            category=category,
            tags=tags,
            read_time=read_time,
            excerpt=excerpt,
            content=content,
            thumbnail_url=thumbnail_url,
            icon=icon or '📝'
        )

        if 'thumbnail' in request.FILES:
            post.thumbnail = request.FILES['thumbnail']

        post.save()
        messages.success(request, f"🎉 Your article '{post.title}' has been published successfully!")
        return redirect('BlogPostDetail', myid=post.post_id)

    return render(request, "blog/create_post.html")


@login_required(login_url='ShopLogin')
def edit_post(request, myid):
    post = get_object_or_404(BlogPost, post_id=myid)
    if post.author_user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this article.")
        return redirect('BlogHome')

    if request.method == 'POST':
        post.title = request.POST.get('title', post.title).strip()
        post.category = request.POST.get('category', post.category).strip()
        post.tags = request.POST.get('tags', post.tags).strip()
        post.read_time = request.POST.get('read_time', post.read_time).strip()
        post.excerpt = request.POST.get('excerpt', post.excerpt).strip()
        post.content = request.POST.get('content', post.content).strip()
        post.thumbnail_url = request.POST.get('thumbnail_url', post.thumbnail_url).strip()
        post.icon = request.POST.get('icon', post.icon).strip()

        if 'thumbnail' in request.FILES:
            post.thumbnail = request.FILES['thumbnail']

        post.save()
        messages.success(request, f"Article '{post.title}' updated successfully!")
        return redirect('BlogPostDetail', myid=post.post_id)

    return render(request, "blog/edit_post.html", {'post': post})


@login_required(login_url='ShopLogin')
def delete_post(request, myid):
    post = get_object_or_404(BlogPost, post_id=myid)
    if post.author_user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to delete this article.")
        return redirect('BlogHome')

    title = post.title
    post.delete()
    messages.success(request, f"Article '{title}' has been deleted.")
    return redirect('BlogHome')
