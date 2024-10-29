from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from perfil.models import Profile, ClientProfile, Publication, ProjectCategory, SocialNetwork, ProjectFreelancer, Project

def calendar(request):
    return render(request, 'perfil/calendar.html')

# Create your views here.
def perfilesFreelancer(request, id):
    
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/perfil_freelancer.html', {'p': p})

def mainFreelancer(request, id):        
    profile = get_object_or_404(Profile, id=id)
    publications_list = Publication.objects.all()
    
    paginator = Paginator(publications_list, 12)  # 12 publicaciones por página
    page_number = request.GET.get('page')  
    publications = paginator.get_page(page_number)
    
    categories = ProjectCategory.objects.all()
    companies = ClientProfile.objects.filter(projects__publications__isnull=False).distinct()
    
    return render(request, 'perfil/main_freelancer.html', {
        'profile': profile,
        'publications': publications,
        'categories': categories,
        'companies': companies
    })

def firstMain(request):
    publications_list = Publication.objects.all()[:3]
    return render(request, 'perfil/main_first.html', {'publications': publications_list})

def projectsList(request, id):
    
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/projects_list.html', {'profile': p})

def projectWorkspace(request, id, id_project):
    p = get_object_or_404(Profile, id=id)
    pr = get_object_or_404(ProjectFreelancer, id=id_project)

    project_data = {
        'id': pr.id,
        'name': pr.name,
        'milestones': [
            {
                'id': milestone.id,
                'name': milestone.name,
                'tasks': [
                    {
                        'name': task.name,
                        'description': task.description
                    }
                    for task in milestone.tasks.all() 
                ]
            }
            for milestone in pr.milestones.all() 
        ],
        'assignments': [
            {
                'name': assignment.name,
                'task': assignment.task.name,
                'date': assignment.date,
                'status': assignment.status,
                'file': assignment.file.url if assignment.file else None,
                'url': assignment.url
            }
            for assignment in pr.assignments.all()
        ]
    }

    return render(request, 'perfil/project_workspace.html', {
        'profile': p,
        'project': project_data,  
    })

def manageProject(request, id, id_project):
    p = get_object_or_404(ClientProfile, id=id)
    pr = get_object_or_404(Project, id=id_project)

    project_data = {
        'id': pr.id,
        'name': pr.name,
        'milestones': [
            {
                'id': milestone.id,
                'name': milestone.name,
                'progress': milestone.progress,
                'deadline': milestone.deadline.strftime('%Y-%m-%d'),  # Formato de fecha
                'tasks': [
                    {
                        'name': task.name
                    }
                    for task in milestone.tasks.all()
                ],
                'freelancer': {
                    'name': milestone.freelancer.name if milestone.freelancer else None,
                    'profile_picture': milestone.freelancer.profile_picture.url if milestone.freelancer and milestone.freelancer.profile_picture else None,
                } if milestone.freelancer else None,
                'applications': [
                    {
                        'freelancer_name': application.freelancer.name,
                        'freelancer_picture': application.freelancer.profile_picture.url if application.freelancer.profile_picture else None,
                    }
                    for application in milestone.applications.all()
                ]
            }
            for milestone in pr.milestones.all()
        ],
        'assignments': [
            {
                'name': assignment.name,
                'task': assignment.task.name,
                'date': assignment.date.strftime('%Y-%m-%d'),  # Formato de fecha
                'status': assignment.status,
                'file': assignment.file.url if assignment.file else None,
                'url': assignment.url
            }
            for assignment in pr.assignments.all()
        ]
    }

    return render(request, 'perfil/client_project_view.html', {
        'profile': p,
        'project': project_data,
    })



def editAccount(request, id):
    p = get_object_or_404(Profile, id=id)

    # Se debe cambiar
    if '-' in p.phone:
        code = p.phone.split('-')[0]
        phone = p.phone.split('-')[1]
    else:
        code = p.phone
        phone = p.phone

    return render(request, 'perfil/edit_profile_account.html', {'p': p, 'code': code, 'phone': phone})

def editAccountClient(request, id):
    p = get_object_or_404(ClientProfile, id=id)

    # Se debe cambiar
    if '-' in p.phone:
        code = p.phone.split('-')[0]
        phone = p.phone.split('-')[1]
    else:
        code = p.phone
        phone = p.phone

    return render(request, 'perfil/client_edit_profile_account.html', {'p': p, 'code': code, 'phone': phone})

def editProfile(request, id=id):
    p = get_object_or_404(Profile, id=id)
    existing_types = p.social_networks.values_list('type', flat=True)
    available_media = [choice for choice in SocialNetwork.TYPE_CHOICES if choice[0] not in existing_types]

    return render(request, 'perfil/edit_profile.html', {'p': p, 'available_media': available_media})

def editProfileClient(request, id=id):
    p = get_object_or_404(ClientProfile, id=id)
    existing_types = p.client_social_networks.values_list('type', flat=True)
    available_media = [choice for choice in SocialNetwork.TYPE_CHOICES if choice[0] not in existing_types]

    return render(request, 'perfil/client_edit_profile.html', {'p': p, 'available_media': available_media})

def deleteDisable(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/edit_profile_delete.html', {'p': p})

def deleteDisableClient(request, id=id):
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/client_edit_profile_delete.html', {'p': p})

def editPortfolio(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/edit_profile_portfolio.html', {'p': p})

def editProjectsClient(request, id=id):
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/client_edit_profile_projects.html', {'p': p})
        
def perfilesCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/perfil_cliente.html', {'p':p})

def mainCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/main_client.html', {'p':p})

def test(request):        
    return render(request, 'perfil/test.html')