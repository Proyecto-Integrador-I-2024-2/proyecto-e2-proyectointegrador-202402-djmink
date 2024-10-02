from django.http import Http404
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from .models import Project

 # get the current user model

# Create your views here.
def freelancerProjectView(request, id):
    p = get_object_or_404(Project, id=id)
    r = p.requirements.all() # get the requirements of the project
    c = p.comments.all() # get the comments of the project
    rating = p.ratings.all().aggregate(Avg('value'))['value__avg'] # get the average rating of the project
    return render(request, 'project_management/freelancer_view.html', {'p': p}, {'r': r}, {'c': c}, {'rating': rating})
            
def clienteProjectView(request, id):        
    p = get_object_or_404(Project, id=id)
    m = p.milestones.all() # get the milestones of the project
    t = p.tasks.all() # get the tasks of the project
    c = p.comments.all() # get the comments of the project
    rating = p.ratings.all().aggregate(Avg('value'))['value__avg'] # get the average rating of the project
    return render(request, 'project_management/client_view.html', {'p':p }, {'m': m}, {'t': t}, {'c': c}, {'rating': rating})
