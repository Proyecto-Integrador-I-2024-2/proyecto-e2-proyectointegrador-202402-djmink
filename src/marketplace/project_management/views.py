from django.http import Http404, JsonResponse
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from my_aplication.models import Project, Freelancer
from .forms import createCommentForm, createRatingForm, createApplicationForm
from django.contrib.contenttypes.models import ContentType

 # get the current user model

def freelancerProjectView2(request):
    return render(request, 'project_management/application_form.html')


# Create your views here.
def freelancerProjectView(request, id):
    p = get_object_or_404(Project, id=id)
    d = p.description # get the description of the project
    r = p.requirements.all() # get the requirements of the project
    c = p.comments.all() # get the comments of the project
    rating = p.ratings.all().aggregate(Avg('value'))['value__avg'] # get the average rating of the project
    context = {
        'p': p,
        'r': r,
        'c': c,
        'd': d,
        'rating': rating
    }
    return render(request, 'project_management/freelancer_view.html', context)
            
def clientProjectView(request, id):        
    p = get_object_or_404(Project, id=id)
    m = p.milestones.all() # get the milestones of the project
    t = p.tasks.all() # get the tasks of the project
    c = p.comments.all() # get the comments of the project
    rating = p.ratings.all().aggregate(Avg('value'))['value__avg'] # get the average rating of the project
    return render(request, 'project_management/client_view.html', {'p':p }, {'m': m}, {'t': t}, {'c': c}, {'rating': rating})

def post_comment(request):
    if request.method == 'POST':
        author = request.POST.get('author', 'Anonymous')  # default if author not provided
        content = request.POST.get('content')
        project_id = request.POST.get('project_id')

        # Make sure to set `project`, `content_type`, and `object_id` appropriately
        # This example assumes you have a valid `project_id` in the POST request
        project = Project.objects.get(id=project_id)
        fct = ContentType.objects.get_for_model(Freelancer)
        user_id = "1"
        
        form = createCommentForm({
            'author': author,
            'content': content,
            'project': project.id,
            'content_type': fct,
            'object_id': user_id,
            'comment': None  # Assuming this is a new top-level comment
        })

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Comment posted successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to post comment'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

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
