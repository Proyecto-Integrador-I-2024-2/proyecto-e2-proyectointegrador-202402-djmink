from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from perfil.models import Profile, ClientProfile, Publication, ProjectCategory, SocialNetwork, ProjectFreelancer, Project

def calendar(request):
    return render(request, 'perfil/calendar.html')

# Create your views here.
def perfilesFreelancer(request, id):
    
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/freelancer_profile.html', {'p': p})

def mainFreelancer(request, id):        
    profile = get_object_or_404(Profile, id=id)
    
    # Obtener el término de búsqueda (si se proporciona)
    search_query = request.GET.get('search', '')
    
    # Filtrar publicaciones por el término de búsqueda
    publications_list = Publication.objects.all()
    if search_query:
        publications_list = publications_list.filter(
            project__name__icontains=search_query
        )
    
    # Filtrar por categoría
    category_id = request.GET.get('category')
    if category_id:
        publications_list = publications_list.filter(project__projectcategories__id=category_id)

    # Filtrar por compañía
    company_id = request.GET.get('company')
    if company_id:
        publications_list = publications_list.filter(profile_id=company_id)  # Filtra directamente por el perfil del cliente

    # Filtrar por presupuesto
    budget = request.GET.get('budget')
    if budget:
        try:
            budget_value = float(budget)
            publications_list = publications_list.filter(project__budget__lte=budget_value)  # Filtra por presupuesto del proyecto
        except ValueError:
            pass  # Maneja el caso en que el presupuesto no es un número válido
    
    # Filtrar por tipo de proyecto
    project_type = request.GET.get('type')  # Obtiene el tipo de proyecto desde la URL
    if project_type:
        publications_list = publications_list.filter(project__type=project_type)

    # Configuración de paginación
    paginator = Paginator(publications_list, 12)  # 12 publicaciones por página
    page_number = request.GET.get('page')  
    publications = paginator.get_page(page_number)

    # Obtener categorías y compañías para los filtros
    categories = ProjectCategory.objects.all()
    companies = ClientProfile.objects.filter(projects__publications__isnull=False).distinct()
    
    return render(request, 'perfil/freelancer_home.html', {
        'profile': profile,
        'publications': publications,
        'categories': categories,
        'companies': companies,
        'search_query': search_query,  # Pasar el término de búsqueda para mostrarlo en el campo
        'budget': budget  # Pasar el presupuesto para mostrarlo en el campo
    })


def firstMain(request):
    publications_list = Publication.objects.all()[:3]
    return render(request, 'perfil/home_page.html', {'publications': publications_list})

def projectsList(request, id):
    
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/freelancer_projects_list.html', {'profile': p})

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

    return render(request, 'perfil/freelancer_project_workspace.html', {
        'profile': p,
        'project': project_data,  
    })

def manageProject(request, id, id_project):
    p = get_object_or_404(ClientProfile, id=id)
    pr = get_object_or_404(Project, id=id_project)

    #progress bar

    total_tasks = 0
    completed_tasks = 0

    for milestone in pr.clientmilestones.all():
        tasks = milestone.tasksclient.all()
        total_tasks += len(tasks)
        completed_tasks += sum(1 for task in tasks if task.state == 'CP')

    project_progress = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    project_data = {
        'id': pr.id,
        'name': pr.name,
        'milestones': [
            {
                'id': milestone.id,
                'name': milestone.name,
                'progress1': milestone.progress,
                'deadline': milestone.deadline.strftime('%Y-%m-%d'),  # Formato de fecha
                'tasks': [
                    {
                        'name': task.name
                    }
                    for task in milestone.tasksclient.all()
                ],
                'freelancer': {
                    'name': milestone.freelancer.name if milestone.freelancer else None,
                    'profile_picture': milestone.freelancer.profile_picture.url if milestone.freelancer and milestone.freelancer.profile_picture else None,
                } if milestone.freelancer else None,
                'applications': [
                    {
                        'freelancer_id': application.freelancer.id,
                        'freelancer_name': application.freelancer.name,
                        'freelancer_picture': application.freelancer.profile_picture.url if application.freelancer.profile_picture else None,
                    }
                    for application in milestone.applications.all()
                ]
            }
            for milestone in pr.clientmilestones.all()
        ],
        'assignments': [
            {
                'name': assignment.name,
                'task': assignment.task.name,
                'milestone_id': assignment.task.milestone.id,
                'freelancer': assignment.task.freelancer.name,
                'date': assignment.date.strftime('%Y-%m-%d'),  # Formato de fecha
                'status': assignment.status,
                'file': assignment.file.url if assignment.file else None,
                'url': assignment.url
            }
            for assignment in pr.assignmentsclient.all()
        ]
    }

    return render(request, 'perfil/client_project_view.html', {
        'profile': p,
        'project_progress': project_progress,
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

    return render(request, 'perfil/freelancer_edit_profile_account.html', {'p': p, 'code': code, 'phone': phone})

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

    return render(request, 'perfil/freelancer_edit_profile.html', {'p': p, 'available_media': available_media})

def editProfileClient(request, id=id):
    p = get_object_or_404(ClientProfile, id=id)
    existing_types = p.client_social_networks.values_list('type', flat=True)
    available_media = [choice for choice in SocialNetwork.TYPE_CHOICES if choice[0] not in existing_types]

    return render(request, 'perfil/client_edit_profile.html', {'p': p, 'available_media': available_media})

def deleteDisable(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/freelancer_edit_profile_delete.html', {'p': p})

def deleteDisableClient(request, id=id):
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/client_edit_profile_delete.html', {'p': p})

def editPortfolio(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/freelancer_edit_profile_portfolio.html', {'p': p})

def editProjectsClient(request, id=id):
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/client_edit_profile_projects.html', {'p': p})
        
def perfilesCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/client_profile.html', {'p':p})

def mainCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/client_projects_list.html', {'p':p})


#ver el perfil de un freelancer:
def freelancerProfile(request, id, idclient):
    # Obtiene el perfil del freelancer usando el id proporcionado
    p = get_object_or_404(Profile, id=id)
    client = get_object_or_404(ClientProfile, id=idclient)
    return render(request, 'perfil/freelancer_profile_view.html', {'p': p, 'client': client})