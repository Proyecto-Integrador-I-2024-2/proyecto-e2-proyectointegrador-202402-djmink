from django.http import Http404
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from .models import Project
from .forms import createCommentForm, createRatingForm, createApplicationForm

 # get the current user model

def freelancerProjectView2(request):
    return render(request, 'project_management/freelancer_view.html')


# Create your views here.
def freelancerProjectView(request, id):
    p = get_object_or_404(Project, id=id)
    r = p.requirements.all() # get the requirements of the project
    c = p.comments.all() # get the comments of the project
    rating = p.ratings.all().aggregate(Avg('value'))['value__avg'] # get the average rating of the project
    return render(request, 'project_management/freelancer_view.html', {'p': p}, {'r': r}, {'c': c}, {'rating': rating})
            
def clientProjectView(request, id):        
    p = get_object_or_404(Project, id=id)
    m = p.milestones.all() # get the milestones of the project
    t = p.tasks.all() # get the tasks of the project
    c = p.comments.all() # get the comments of the project
    rating = p.ratings.all().aggregate(Avg('value'))['value__avg'] # get the average rating of the project
    return render(request, 'project_management/client_view.html', {'p':p }, {'m': m}, {'t': t}, {'c': c}, {'rating': rating})

def createComment(request, id):
    p = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = createCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.project = p
            c.save()
            return render(request, 'project_management/client_view.html', {'p':p})
    else:
        form = createCommentForm()
    return render(request, 'project_management/create_comment.html', {'form': form})

def createRating(request, id):
    p = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = createRatingForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.project = p
            r.save()
            return render(request, 'project_management/client_view.html', {'p':p})
    else:
        form = createRatingForm()
    return render(request, 'project_management/create_rating.html', {'form': form})

def createApplication(request, id):
    p = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = createApplicationForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.project = p
            a.save()
            return render(request, 'project_management/client_view.html', {'p':p})
    else:
        form = createApplicationForm()
    return render(request, 'project_management/create_application.html', {'form': form})
