from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # for queryset filter
from .models import Post, CV, Work, Education # include the model written previously
from .forms import PostForm, CVForm, WorkForm, EducationForm

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

    if request.method == "POST":# Accessing page for the first time an we want a blank form
        form = PostForm(request.POST)
        if form.is_valid():# Checking if the form is correct
            # Saving it
            post = form.save(commit=False)# false means we don't want to save the post model yet
            post.author = request.user
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
    works = Work.objects.all()
    educations = Education.objects.all()
    # if (cv is None):
    #     cv = CV.objects.create(author=request.user)

    return render(request, 'blog/cv_page.html', {"cv": cv, "works": works, "educations": educations})

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

def work_add(request):
    if not request.user.is_authenticated:
        return redirect('cv_page')

    if request.method == "POST":# Accessing page for the first time an we want a blank form
        form = WorkForm(request.POST)
        if form.is_valid():# Checking if the form is correct
            # Saving it
            work = form.save(commit=False)# false means we don't want to save the post model yet
            work.author = request.user
            work.save()
            return redirect('cv_page')# redirects us to the new post
    else:# we go back to the view with all the form data we just typed
        form = WorkForm()
    return render(request, 'blog/work_edit.html', {'form': form})

def work_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('cv_page')

    work = get_object_or_404(Work, pk=pk)

    if request.method == "POST":
        form = WorkForm(request.POST, instance=work)
        if form.is_valid():
            work = form.save(commit=False)
            work.author = request.user
            work.save()
            return redirect('cv_page')
    else:
        form = WorkForm(instance=work)
    return render(request,'blog/work_edit.html',{'form': form})

def education_add(request):
    if not request.user.is_authenticated:
        return redirect('cv_page')

    if request.method == "POST":# Accessing page for the first time an we want a blank form
        form = EducationForm(request.POST)
        if form.is_valid():# Checking if the form is correct
            # Saving it
            education = form.save(commit=False)# false means we don't want to save the post model yet
            education.author = request.user
            education.save()
            return redirect('cv_page')# redirects us to the new post
    else:# we go back to the view with all the form data we just typed
        form = EducationForm()
    return render(request,'blog/education_edit.html', {'form': form})

def education_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('cv_page')

    education = get_object_or_404(Education, pk=pk)

    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            education = form.save(commit=False)
            education.author = request.user
            education.save()
            return redirect('cv_page')
    else:
        form = EducationForm(instance=education)
    return render(request,'blog/education_edit.html',{'form': form})
