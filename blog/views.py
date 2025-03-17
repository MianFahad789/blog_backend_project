from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import Count,Avg
from .models import BlogPost, Category,Like,Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import BlogPostForm  
from django.contrib import messages
from .forms import ReaderRegistrationForm,PublisherRegistrationForm

def blog_list(request):
    category_id = request.GET.get('category')
    blogs = BlogPost.objects.all()

    if category_id:
        blogs = blogs.filter(category_id=category_id)

    sort_by = request.GET.get('sort_by')

    if sort_by == 'recent':
        blogs = blogs.order_by('-created_at')
    elif sort_by == 'most_liked':
        blogs = blogs.annotate(num_likes=Count('likes')).order_by('-num_likes')
    elif sort_by == 'latest':  # Sort by latest created blog
        blogs = blogs.order_by('-created_at')
    elif sort_by == 'earliest':  # Sort by earliest created blog
        blogs = blogs.order_by('created_at')

    categories = Category.objects.all()
    
    paginator = Paginator(blogs, 5)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })



def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    blog.views += 1  # Increment views
    blog.save()

    # Calculate average rating
    avg_rating = blog.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Check if the current user has liked the blog
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, blog_post=blog).exists()

    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'avg_rating': round(avg_rating, 2),
        'user_liked': user_liked,
    })

def like_blog(request, pk):
    if request.user.is_authenticated:
        blog = get_object_or_404(BlogPost, pk=pk)
        Like.objects.get_or_create(user=request.user, blog_post=blog)
    return redirect('blog_detail', pk=pk)

def add_review(request, pk):
    if request.user.is_authenticated and request.method == 'POST':
        blog = get_object_or_404(BlogPost, pk=pk)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(user=request.user, blog_post=blog, rating=rating, comment=comment)
    return redirect('blog_detail', pk=pk)

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Registration successful!')
#             return redirect('blog_list')
#     else:
#         form = UserCreationForm()
#     return render(request, 'blog/register.html', {'form': form})

@login_required
def publisher_dashboard(request):
    if not request.user.is_publisher:
        return redirect('blog_list')
    blogs = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/publisher_dashboard.html', {'blogs': blogs})

@login_required
def create_blog(request):
    if not request.user.is_publisher:
        return redirect('blog_list')  # Only publishers can create blogs

    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Set the author to the current user
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogPostForm()

    return render(request, 'blog/create_blog.html', {'form': form})


def register_reader(request):
    if request.method == 'POST':
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in as a reader.')
            return redirect('blog_list')
    else:
        form = ReaderRegistrationForm()
    return render(request, 'blog/register_reader.html', {'form': form})

def register_publisher(request):
    if request.method == 'POST':
        form = PublisherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in as a publisher.')
            return redirect('blog_list')
    else:
        form = PublisherRegistrationForm()
    return render(request, 'blog/register_publisher.html', {'form': form})


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('blog_list')  # Redirect to the blog list after adding a category
    return render(request, 'blog/add_category.html')