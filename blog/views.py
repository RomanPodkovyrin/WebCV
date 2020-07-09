from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # for queryset filter
from .models import Post, CV # include the model written previously
from .forms import PostForm, CVForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if not request.user.is_authenticated:
        return redirect('post_list')

    # print('hello')
    if request.method == "POST":# Accessing page for the first time an we want a blank form
        # print('Post')
        form = PostForm(request.POST)
        if form.is_valid():# Checking if the form is correct
            # print('Valid')
            # Saving it
            post = form.save(commit=False)# false means we don't want to save the post model yet
            # print(post.pk)
            post.author = request.user
            # print('User', post.author)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)# redirects us to the new post
    else:# we go back to the view with all the form data we just typed
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('post_list')

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def cv_page(request):
    cv = CV.objects.first()
    # if (cv is None):
    #     cv = CV.objects.create(author=request.user)

    return render(request, 'blog/cv_page.html', {"cv": cv})

def cv_edit(request):
    if not request.user.is_authenticated:
        return redirect('cv_page')

    # cv = get_object_or_404(CV)
    cv = CV.objects.first()
    # if (cv is None):
    #     cv = CV.objects.create(author=request.user)
    if request.method == "POST":
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.author = request.user
            cv.save()
            return redirect('cv_page')
    else:
        form = CVForm(instance=cv)
    return render(request, 'blog/cv_edit.html', {'form': form})

def work_list(request):
    return render(request, 'blog/work_list.html', {})

def work_add(request):
    if not request.user.is_authenticated:
        return redirect('cv_page')
    return render(request, 'blog/work_edit.html', {})