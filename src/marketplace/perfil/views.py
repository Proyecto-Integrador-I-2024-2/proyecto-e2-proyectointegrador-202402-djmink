from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from my_aplication.models import Freelancer, CompanyManager, ProjectCategory, SocialNetwork, Project, Skill, Certificate


def calendar(request):
    return render(request, 'perfil/calendar.html')

# Create your views here.
def perfilesFreelancer(request, id):
    p = get_object_or_404(Freelancer, id=id)
    return render(request, 'perfil/freelancer_profile.html', {'p': p})

def mainFreelancer(request, id):
    profile = get_object_or_404(Freelancer, id=id)

    # Obtener el término de búsqueda (si se proporciona)
    search_query = request.GET.get('search', '')

    # Filtrar proyectos por el término de búsqueda
    projects_list = Project.objects.all()
    print(projects_list)
    if search_query:
        projects_list = projects_list.filter(name__icontains=search_query)

    # Filtrar por categoría
    category_id = request.GET.get('category')
    if category_id:
        projects_list = projects_list.filter(projectcategories__id=category_id)

    # Filtrar por compañía
    company_id = request.GET.get('company')
    if company_id:
        projects_list = projects_list.filter(clientprofile__id=company_id)  # Asegúrate de usar 'clientprofile' correctamente

    # Filtrar por presupuesto
    budget = request.GET.get('budget')
    if budget:
        try:
            budget_value = float(budget)
            projects_list = projects_list.filter(budget__lte=budget_value)  # Filtra por presupuesto del proyecto
        except ValueError:
            pass  # Maneja el caso en que el presupuesto no es un número válido

    # Filtrar por tipo de proyecto
    project_type = request.GET.get('type')  # Obtiene el tipo de proyecto desde la URL
    if project_type:
        projects_list = projects_list.filter(type=project_type)

    # Configuración de paginación
    paginator = Paginator(projects_list, 12)  # 12 proyectos por página
    page_number = request.GET.get('page')  
    projects = paginator.get_page(page_number)  # Cambié 'publications' a 'projects'

    # Obtener categorías y compañías para los filtros
    categories = ProjectCategory.objects.all()
    companies = CompanyManager.objects.filter(projects__isnull=False).distinct()

    return render(request, 'perfil/freelancer_home.html', {
        'profile': profile,
        'projects': projects,  # Asegúrate de pasar 'projects'
        'categories': categories,
        'companies': companies,
        'search_query': search_query,  # Pasar el término de búsqueda para mostrarlo en el campo
        'budget': budget  
    })


def firstMain(request):
    publications_list = Project.objects.all()[:3]
    return render(request, 'perfil/home_page.html', {'publications': publications_list})

def projectsList(request, id):
    p = get_object_or_404(Freelancer, id=id)
    return render(request, 'perfil/freelancer_projects_list.html', {'profile': p})

def projectWorkspace(request, id, id_project):
    p = get_object_or_404(Freelancer, id=id)
    pr = get_object_or_404(Freelancer, id=id_project)

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
    p = get_object_or_404(CompanyManager, id=id)
    pr = get_object_or_404(Project, id=id_project)

    #progress bar

    total_tasks = 0
    completed_tasks = 0

    for milestone in pr.milestones.all():
        tasks = milestone.tasks.all()
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
                    for task in milestone.tasks.all()
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
            for milestone in pr.milestones.all()
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
            for assignment in pr.assignments.all()
        ]
    }

    return render(request, 'perfil/client_project_view.html', {
        'profile': p,
        'project_progress': project_progress,
        'project': project_data,
    })


def editProfile(request, id=id):
    p = get_object_or_404(Freelancer, id=id)

    existing_types = p.social_networks.values_list('type', flat=True)
    available_media = [choice for choice in SocialNetwork.TYPE_CHOICES if choice[0] not in existing_types]

    if request.method == 'POST':

        p.image = request.FILES.get('image', p.image)
        p.profession = request.POST.get('profession', p.profession)
        p.description = request.POST.get('description', p.description)
        p.contact_email = request.POST.get('contact_email', p.contact_email)
        p.experience = request.POST.get('experience', p.experience)
        p.price = request.POST.get('price', p.price)
        
        removed_social_ids = request.POST.get('removed_social_ids', '')
        if removed_social_ids:
            for social_id in removed_social_ids.split(','):
                try:
                    social_network = SocialNetwork.objects.get(id=int(social_id), profile=p)
                    social_network.delete()
                except SocialNetwork.DoesNotExist:
                    continue

        social_ids = request.POST.getlist('social_id')
        for social_id in social_ids:
            social_url = request.POST.get(f'social_url_{social_id}')
            social_type = request.POST.get(f'social_type_{social_id}')

            if social_url and social_id not in removed_social_ids.split(','):
                social_network, created = SocialNetwork.objects.get_or_create(
                    profile=p,
                    type=social_type,
                    defaults={'url': social_url} 
                )
                if not created:
                    social_network.url = social_url
                    social_network.save()

        removed_skill_ids = request.POST.get('removed_skill_ids', '')
        if removed_skill_ids:
            for skill_id in removed_skill_ids.split(','):
                try:
                    skill = Skill.objects.get(id=int(skill_id), profile=p)
                    skill.delete()
                except Skill.DoesNotExist:
                    continue

        skill_ids = request.POST.getlist('skill_id')
        for skill_id in skill_ids:
            skill_name = request.POST.get(f'skill_name_{skill_id}')
            if skill_id not in removed_skill_ids.split(','):
                if skill_name:
                    try:
                        skill = Skill.objects.get(id=int(skill_id), profile=p)
                        skill.name = skill_name
                        skill.save()
                    except Skill.DoesNotExist:
                        Skill.objects.create(profile=p, name=skill_name)

        removed_certificate_ids = request.POST.get('removed_certificate_ids', '')
        if removed_certificate_ids:
            for certificate_id in removed_certificate_ids.split(','):
                try:
                    certificate = Certificate.objects.get(id=int(certificate_id), profile=p)
                    certificate.delete()
                except Certificate.DoesNotExist:
                    continue
        
        certificate_ids = request.POST.getlist('certificate_id')
        for certificate_id in certificate_ids:
            certificate_name = request.POST.get(f'certificate_name_{certificate_id}')
            certificate_type = request.POST.get(f'certificate_type_{certificate_id}')
            certificate_url = request.POST.get(f'certificate_url_{certificate_id}')

            if certificate_id not in removed_certificate_ids.split(','):
                if certificate_name and certificate_type and certificate_url:
                    certificate = Certificate.objects.get_or_create(
                        profile=p,
                        name=certificate_name,
                        type=certificate_type,
                        defaults={'url': certificate_url}
                    )

        p.save()

        return redirect('editProfile', id=id)

    return render(request, 'perfil/freelancer_edit_profile.html', {'p': p, 'available_media': available_media})


def editProfileClient(request, id=id):
    p = get_object_or_404(CompanyManager, id=id)
    existing_types = p.client_social_networks.values_list('type', flat=True)
    available_media = [choice for choice in SocialNetwork.TYPE_CHOICES if choice[0] not in existing_types]

    return render(request, 'perfil/client_edit_profile.html', {'p': p, 'available_media': available_media})

def deleteDisable(request, id=id):
    p = get_object_or_404(Freelancer, id=id)
    return render(request, 'perfil/freelancer_edit_profile_delete.html', {'p': p})

def deleteDisableClient(request, id=id):
    p = get_object_or_404(CompanyManager, id=id)
    return render(request, 'perfil/client_edit_profile_delete.html', {'p': p})

def editPortfolio(request, id=id):
    p = get_object_or_404(Freelancer, id=id)
    return render(request, 'perfil/freelancer_edit_profile_portfolio.html', {'p': p})

def editProjectsClient(request, id=id):
    p = get_object_or_404(CompanyManager, id=id)
    return render(request, 'perfil/client_edit_profile_projects.html', {'p': p})
        
def perfilesCliente(request, id):        
    p = get_object_or_404(CompanyManager, id=id)
    return render(request, 'perfil/client_profile.html', {'p':p})

def mainCliente(request, id):        
    p = get_object_or_404(CompanyManager, id=id)
    return render(request, 'perfil/client_projects_list.html', {'p':p})

def editAccount(request, id):
    p = get_object_or_404(Freelancer, id=id)

    # Se debe cambiar
    if '-' in p.phone:
        code = p.phone.split('-')[0]
        phone = p.phone.split('-')[1]
    else:
        code = p.phone
        phone = p.phone

    return render(request, 'perfil/freelancer_edit_profile_account.html', {'p': p, 'code': code, 'phone': phone})

def editAccountClient(request, id):
    p = get_object_or_404(CompanyManager, id=id)

    # Se debe cambiar
    if '-' in p.phone:
        code = p.phone.split('-')[0]
        phone = p.phone.split('-')[1]
    else:
        code = p.phone
        phone = p.phone

    return render(request, 'perfil/client_edit_profile_account.html', {'p': p, 'code': code, 'phone': phone})


#ver el perfil de un freelancer:
def freelancerProfile(request, id, idclient):
    # Obtiene el perfil del freelancer usando el id proporcionado
    p = get_object_or_404(Freelancer, id=id)
    client = get_object_or_404(CompanyManager, id=idclient)
    return render(request, 'perfil/freelancer_profile_view.html', {'p': p, 'client': client})