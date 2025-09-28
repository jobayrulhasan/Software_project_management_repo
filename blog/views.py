from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.views import View
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Show all blog posts
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

# Show single post
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        name = request.POST.get('name')
        text = request.POST.get('text')
        Comment.objects.create(post=post, name=name, text=text)
        messages.success(request, 'Comment added successfully!')
        return redirect('post_detail', post_id=post_id)

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


# class view for user registration
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'blog/customerregistration.html', {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! registration successfull')
            return render(request, 'blog/customerregistration.html', {'form': form})


# user login
def user_login(request):
    if request.method == 'POST':
        frm = AuthenticationForm(request=request, data=request.POST)
        if frm.is_valid():
            uName = frm.cleaned_data.get('username')
            uPassword = frm.cleaned_data.get('password')
            user = authenticate(username=uName, password=uPassword)
            if user is not None:
                login(request, user)
                return redirect('/') # profile is the name of url's name
    else:
      frm = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': frm})

# user logout
def user_logout(request):
    logout(request)
    return redirect('/')

# Create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(author=request.user, title=title, content=content, image=image)
        messages.success(request, 'Post created successfully!')
        return redirect('home')

    return render(request, 'blog/create_post.html')

# Edit a post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        messages.success(request, 'Post updated successfully!')
        return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/edit_post.html', {'post': post})

# Delete a post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('home')
