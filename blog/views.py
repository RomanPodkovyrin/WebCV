from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # for queryset filter
from .models import Post, CV, Work, Education, Skill # include the model written previously
from .forms import PostForm, CVForm, WorkForm, EducationForm, SkillForm

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
    skills = Skill.objects.all()
    # if (cv is None):
    #     cv = CV.objects.create(author=request.user)

    return render(request, 'blog/cv_page.html', {"cv": cv, "works": works, "educations": educations, "skills": skills})

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
    return render(request, 'blog/cv_edit.html', {'form': form, 'title':"Editing CV"})

def new_element(request, page_form, title):
    if not request.user.is_authenticated:
        return redirect('cv_page')

    if request.method == "POST":# Accessing page for the first time an we want a blank form
        form = page_form(request.POST)
        if form.is_valid():# Checking if the form is correct
            # Saving it
            element = form.save(commit=False)# false means we don't want to save the post model yet
            element.author = request.user
            element.save()
            return redirect('cv_page')# redirects us to the new post
    else:# we go back to the view with all the form data we just typed
        form = page_form()
    return render(request, 'blog/cv_edit.html', {'form': form, 'title':title})

def edit_element(request, pk, model, page_form, title):
    if not request.user.is_authenticated:
        return redirect('cv_page')

    element = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        form = page_form(request.POST, instance=element)
        if form.is_valid():
            element = form.save(commit=False)
            element.author = request.user
            element.save()
            return redirect('cv_page')
    else:
        form = page_form(instance=element)
    return render(request,'blog/cv_edit.html',{'form': form, 'title':title})

def work_add(request):
    return new_element(request, WorkForm, "Adding New Work Experience" )

def work_edit(request, pk):
    return edit_element(request, pk, Work, WorkForm,"Editing Work Experinece" )

def education_add(request):
    return new_element(request, EducationForm, "Adding New Education" )

def education_edit(request, pk):
    return edit_element(request, pk, Education, EducationForm, "Editing Education")

def skill_add(request):
    return new_element(request, SkillForm, "Adding New Skill" )

def skill_edit(request, pk):
    return edit_element(request, pk, Skill, SkillForm, "Editing Skill")