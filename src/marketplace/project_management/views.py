from django.http import Http404, JsonResponse
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from my_aplication.models import Project, Freelancer, Milestone, Like
from .forms import createCommentForm, createRatingForm, createApplicationForm
from django.contrib.contenttypes.models import ContentType

 # get the current user model

def freelancerProjectView2(request):
    return render(request, 'project_management/application_form.html')


# Create your views here.
def freelancerProjectView(request, freelancer_id, id):
    p = get_object_or_404(Project, id=id)
    f = get_object_or_404(Freelancer, id=freelancer_id)
    d = p.description # get the description of the project
    m = p.milestones.all() # get the milestones of the project
    c = p.comments.all() # get the comments of the project
    likes = p.likes.count() # get the likes of the project
    rating = p.ratings.all().aggregate(Avg('value'))['value__avg'] # get the average rating of the project
    has_applied = p.applications.filter(freelancer=f).exists()
    f.profile_url = reverse('perfilFreelancer', args=[f.id])
    f.has_liked = p.likes.filter(object_id=f.id).exists()
    f.has_applied = has_applied

    for comment in c:
        comment.profile_url = reverse('perfilFreelancer', args=[comment.user.id])

    context = {
        'p': p,
        'm': m,
        'c': c,
        'd': d,
        'profile_url': reverse('perfilesCliente', args=[p.manager.id]),
        'rating': rating,
        'likes': likes,
        'freelancer': f,
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
        freelancer_id = request.POST.get('freelancer_id')

        # Make sure to set `project`, `content_type`, and `object_id` appropriately
        # This example assumes you have a valid `project_id` in the POST request

        project = Project.objects.get(id=project_id)
        fct = ContentType.objects.get_for_model(Freelancer)
        
        form = createCommentForm({
            'author': author,
            'content': content,
            'project': project.id,
            'content_type': fct,
            'object_id': freelancer_id,
            'comment': None  # Assuming this is a new top-level comment
        })

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Comment posted successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to post comment'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def post_like(request):
    if request.method == 'POST':
        like = request.POST.get('like')
        project_id = request.POST.get('project_id')
        freelancer_id = request.POST.get('freelancer_id')

        fct = ContentType.objects.get_for_model(Freelancer)
        project = Project.objects.get(id=project_id)

        if like == 'true':
            like = Like.objects.create(project=project, object_id=freelancer_id, content_type=fct)
            return JsonResponse({'success': True, 'message': 'Liked successfully'})
        else:
            like = Like.objects.filter(project=project, object_id=freelancer_id).delete()
            return JsonResponse({'success': True, 'message': 'Unliked successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
    

def post_application(request):
    if request.method == 'POST':
        freelancer_id = request.POST.get('freelancer_id')
        project_id = request.POST.get('project_id')
        milestone_id = request.POST.get('milestone_id')

        project = Project.objects.get(id=project_id)
        freelancer = Freelancer.objects.get(id=freelancer_id)
        milestone = Milestone.objects.get(id=milestone_id)

        form = createApplicationForm({
            'milestone': milestone,
            'project': project,
            'freelancer': freelancer
        })

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Application posted successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to post application'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
