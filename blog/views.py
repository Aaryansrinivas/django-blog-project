from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import postform
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef
from .models import Post, Comment, Like
#from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Value, BooleanField
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef


def home(request):
    user = request.user
    posts = Post.objects.prefetch_related('comments', 'likes').order_by('-date_created')

    if user.is_authenticated:
        liked_posts = Like.objects.filter(post=OuterRef('pk'), user=user)
        posts = posts.annotate(user_liked=Exists(liked_posts))

       
    else:
        posts = Post.objects.annotate(is_favorite=Value(False, output_field=BooleanField()))
        profile = None

    # Pagination
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        #'profile': profile,
    }

    return render(request, 'blog/home.html', context)


   
    
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')  # Most recent comments first

    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('comment', '').strip()
            if content:
                Comment.objects.create(post=post, author=request.user, content=content)
                return redirect('post_detail', post_id)
        else:
            return redirect('login')  # Prevent anonymous users from commenting

    context = {
        'post': post,
        'comments': comments,
        'liked': liked,
    }
    return render(request, 'blog/post_detail.html', context)


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})




@login_required
def post_new(request):
    if request.method == "POST":
        form = postform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = postform()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = postform(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = postform(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

    
@login_required
def post_delete (request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=="POST":
        post.delete()
        return redirect('home')
    return render(request,'blog/post_delete.html',{'post':post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # ✅ Corrected line
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # Toggle like
    return redirect('post_detail', post_id=post.id)






    
    
