from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from my_aplication.models import Freelancer, CompanyManager, ProjectCategory, SocialNetwork, Project, Skill, Certificate, Content, User, CommentProfile, Rating, Application, Assignment, Task, Milestone
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.db.models import Avg
from datetime import datetime

def editAccountClient(request, id):

    p = get_object_or_404(CompanyManager, id=id)

    profile_changed = False
    password_changed = False
    password_error = False

    if request.method == "POST":
       
        new_username = request.POST.get('username', p.username)
        new_name = request.POST.get('name', p.name)
        new_email = request.POST.get('email', p.email)
        new_phone = request.POST.get('phone', p.phone)

        if User.objects.filter(username=new_username).exclude(id=p.id).exists():
            messages.error(request, "El nombre de usuario ya está en uso. Por favor elige otro.")
            return render(request, 'perfil/client_edit_profile_account.html', {'p': p})

        if p.username != new_username:
            p.username = new_username
            profile_changed = True
        if p.name != new_name:
            p.name = new_name
            profile_changed = True
        if p.email != new_email:
            p.email = new_email
            profile_changed = True
        if p.phone != new_phone:
            p.phone = new_phone
            profile_changed = True

        if profile_changed:
            p.save()
            messages.success(request, "El perfil se actualizó correctamente.")

        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        if current_password or new_password or confirm_password:
            if new_password != confirm_password:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                password_error = True
            else:
                if not p.check_password(current_password):
                    messages.error(request, "La contraseña actual es incorrecta.")
                    password_error = True
                else:
                    p.set_password(new_password)
                    p.save()
                    update_session_auth_hash(request, p)
                    messages.success(request, "La contraseña se actualizó correctamente.")
                    password_changed = True
        else:
            password_changed = False

        if not profile_changed and not password_changed and not password_error:
            messages.info(request, "No se han detectado cambios.")

        if profile_changed or password_changed or password_error:
            return redirect('editAccountClient', id=id)


    profile_url = reverse('perfilesCliente', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/client_edit_profile_account.html', {
        'p': p, 
        'home_url': reverse('mainCliente', args=[p.id]),
        'at_client_page': True,
        'profile_url': profile_url, 
        'profile_image': profile_image})

def editAccount(request, id):
    p = get_object_or_404(Freelancer, id=id)

    profile_changed = False
    password_changed = False
    password_error = False

    if request.method == "POST":
       
        new_username = request.POST.get('username', p.username)
        new_name = request.POST.get('name', p.name)
        new_email = request.POST.get('email', p.email)
        new_phone = request.POST.get('phone', p.phone)

        if User.objects.filter(username=new_username).exclude(id=p.id).exists():
            messages.error(request, "El nombre de usuario ya está en uso. Por favor elige otro.")
            return render(request, 'perfil/freelancer_edit_profile_account.html', {'p': p})

        if p.username != new_username:
            p.username = new_username
            profile_changed = True
        if p.name != new_name:
            p.name = new_name
            profile_changed = True
        if p.email != new_email:
            p.email = new_email
            profile_changed = True
        if p.phone != new_phone:
            p.phone = new_phone
            profile_changed = True

        if profile_changed:
            p.save()
            messages.success(request, "El perfil se actualizó correctamente.")

        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        if current_password or new_password or confirm_password:
            if new_password != confirm_password:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                password_error = True
            else:
                if not p.check_password(current_password):
                    messages.error(request, "La contraseña actual es incorrecta.")
                    password_error = True
                else:
                    p.set_password(new_password)
                    p.save()
                    update_session_auth_hash(request, p)
                    messages.success(request, "La contraseña se actualizó correctamente.")
                    password_changed = True
        else:
            password_changed = False

        if not profile_changed and not password_changed and not password_error:
            messages.info(request, "No se han detectado cambios.")

        if profile_changed or password_changed or password_error:
            return redirect('editAccount', id=id)


    profile_url = reverse('perfilFreelancer', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/freelancer_edit_profile_account.html', {
        'p': p,
        'projects_url': reverse('projectsList', args=[p.id]),
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'profile_image': profile_image,
        'profile_url': profile_url})

def perfilesCliente(request, id):        
    p = get_object_or_404(CompanyManager, id=id)

    if request.method == 'POST':
    
        action = request.POST.get('action')
        
        if action == 'create_comment':
            content = request.POST.get('content')
            reply_to_id = request.POST.get('reply_to')

            if not content:
                messages.error(request, "No puede enviar una respuesta vacía.")
                return redirect('perfilesCliente', id=id)
            
            if reply_to_id:
                reply_to_comment = CommentProfile.objects.get(id=reply_to_id)
                new_comment = CommentProfile.objects.create(
                    user_profile=p,
                    author=p,
                    content=content,
                    reply_to=reply_to_comment
                )

            new_comment.save()
            messages.success(request, "Respuesta enviada exitosamente.")
            return redirect('perfilesCliente', id=id)

        elif action == 'edit_comment':
            comment_id = request.POST.get('comment_id')
            content = request.POST.get('new_content')

            if not content:
                messages.error(request, "No puede dejar una respuesta vacía.")
                return redirect('perfilesCliente', id=id)
            
            comment = CommentProfile.objects.get(id=comment_id, author=p)
            comment.content = content
            comment.save()
            messages.success(request, "Respuesta editada exitosamente.")
            
            return redirect('perfilesCliente', id=id)

        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id')
            
            comment = CommentProfile.objects.get(id=comment_id, author=p)
            comment.delete()
            messages.success(request, "Respuesta eliminada exitosamente.")
            
            return redirect('perfilesCliente', id=id)

    profile_url = reverse('perfilesCliente', args=[p.id])
    edit_profile_url = reverse('editAccountClient', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/client_profile.html', {
        'p':p,
        'home_url': reverse('mainCliente', args=[p.id]),
        'at_client_page': True,
        'edit_profile_url': edit_profile_url,
        'profile_url': profile_url,
        'profile_image': profile_image,
        'can_rate': False,
        'show_edit_link': True})

def perfilesFreelancer(request, id):

    p = get_object_or_404(Freelancer, id=id)

    if request.method == 'POST':
    
        action = request.POST.get('action')
        
        if action == 'create_comment':
            content = request.POST.get('content')
            reply_to_id = request.POST.get('reply_to')

            if not content:
                messages.error(request, "No puede enviar una respuesta vacía.")
                return redirect('perfilFreelancer', id=id)
            
            if reply_to_id:
                reply_to_comment = CommentProfile.objects.get(id=reply_to_id)
                new_comment = CommentProfile.objects.create(
                    user_profile=p,
                    author=p,
                    content=content,
                    reply_to=reply_to_comment
                )

            new_comment.save()
            messages.success(request, "Respuesta enviada exitosamente.")
            return redirect('perfilFreelancer', id=id)

        elif action == 'edit_comment':
            comment_id = request.POST.get('comment_id')
            content = request.POST.get('new_content')

            if not content:
                messages.error(request, "No puede dejar una respuesta vacía.")
                return redirect('perfilFreelancer', id=id)
            
            comment = CommentProfile.objects.get(id=comment_id, author=p)
            comment.content = content
            comment.save()
            messages.success(request, "Respuesta editada exitosamente.")
            
            return redirect('perfilFreelancer', id=id)

        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id')
            
            comment = CommentProfile.objects.get(id=comment_id, author=p)
            comment.delete()
            messages.success(request, "Respuesta eliminada exitosamente.")
            
            return redirect('perfilFreelancer', id=id) 

    profile_url = reverse('perfilFreelancer', args=[p.id])
    edit_profile_url = reverse('editAccount', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/freelancer_profile.html', {
        'p':p,
        'projects_url': reverse('projectsList', args=[p.id]),
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'edit_profile_url': edit_profile_url,
        'profile_image': profile_image, 
        'profile_url': profile_url,
        'can_rate': False,
        'show_edit_link': True})

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
        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('editProfile', id=id)

    profile_image = p.image.url
    profile_url = reverse('perfilFreelancer', args=[p.id])
    return render(request, 'perfil/freelancer_edit_profile.html', {
        'p': p,
        'projects_url': reverse('projectsList', args=[p.id]),
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'profile_image': profile_image,
        'profile_url': profile_url, 
        'available_media': available_media})


def editProfileClient(request, id=id):
    p = get_object_or_404(CompanyManager, id=id)
    existing_types = p.client_social_networks.values_list('type', flat=True)
    available_media = [choice for choice in SocialNetwork.TYPE_CHOICES if choice[0] not in existing_types]

    if request.method == 'POST':

        p.image = request.FILES.get('image', p.image)
        p.company_type = request.POST.get('type', p.company_type)
        p.description = request.POST.get('description', p.description)
        p.contact_email = request.POST.get('contact_email', p.contact_email)
        
        removed_social_ids = request.POST.get('removed_social_ids', '')
        if removed_social_ids:
            for social_id in removed_social_ids.split(','):
                try:
                    social_network = SocialNetwork.objects.get(id=int(social_id), client_profile=p)
                    social_network.delete()
                except SocialNetwork.DoesNotExist:
                    continue

        social_ids = request.POST.getlist('social_id')
        for social_id in social_ids:
            social_url = request.POST.get(f'social_url_{social_id}')
            social_type = request.POST.get(f'social_type_{social_id}')

            if social_url and social_id not in removed_social_ids.split(','):
                social_network, created = SocialNetwork.objects.get_or_create(
                    client_profile=p,
                    type=social_type,
                    defaults={'url': social_url} 
                )
                if not created:
                    social_network.url = social_url
                    social_network.save()

        p.save()
        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('editProfileClient', id=id)

    profile_url = reverse('perfilesCliente', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/client_edit_profile.html', {
        'p': p,
        'profile_url': profile_url,
        'home_url': reverse('mainCliente', args=[p.id]),
        'at_client_page': True,
        'profile_image': profile_image, 
        'available_media': available_media})

def editPortfolio(request, id=id):
    p = get_object_or_404(Freelancer, id=id)

    if request.method == 'POST':
        
        removed_project_ids = request.POST.get('removed_project_ids', '')
        if removed_project_ids:
            for project_id in removed_project_ids.split(','):
                try:
                    project = Content.objects.get(id=int(project_id), profile=p)
                    project.delete()
                except Content.DoesNotExist:
                    continue

        project_ids = request.POST.getlist('project_id')
        for project_id in project_ids:

            project_name = request.POST.get(f'project_name_{project_id}')
            project_company = request.POST.get(f'project_company_{project_id}')
            project_duration = request.POST.get(f'project_duration_{project_id}')
            project_url = request.POST.get(f'project_url_{project_id}')

            if project_id not in removed_project_ids.split(','):
                try:
                    project = Content.objects.get(id=int(project_id), profile=p)
                    project.name = project_name
                    project.type = project_company
                    project.duration = project_duration
                    project.url = project_url
                    project.save()
                except Content.DoesNotExist:
                    Content.objects.create(
                        profile=p,
                        name=project_name,
                        type=project_company,
                        duration=project_duration,
                        url=project_url
                    )

        p.save()
        messages.success(request, "Portafolio actualizado exitosamente.")
        return redirect('editPortfolio', id=id)
    
    profile_url = reverse('perfilFreelancer', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/freelancer_edit_profile_portfolio.html', {
        'p': p,
        'projects_url': reverse('projectsList', args=[p.id]),
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'profile_image': profile_image,
        'profile_url': profile_url})

def editProjectsClient(request, id=id):
    p = get_object_or_404(CompanyManager, id=id)

    if request.method == 'POST':
        
        removed_project_ids = request.POST.get('removed_project_ids', '')
        if removed_project_ids:
            for project_id in removed_project_ids.split(','):
                try:
                    project = Project.objects.get(id=int(project_id), manager=p)

                    if project.state == 'IN_PROGRESS':
                        messages.error(request, f"El proyecto '{project.name}' está en desarrollo y no se puede eliminar.")
                        continue

                    project.delete()
                    messages.success(request, f"El proyecto '{project.name}' fue eliminado exitosamente.")

                except Project.DoesNotExist:
                    continue
            
            return redirect('editProjectsClient', id=id)

    profile_url = reverse('perfilesCliente', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/client_edit_profile_projects.html', {
        'p': p,
        'profile_url': profile_url,
        'home_url': reverse('mainCliente', args=[p.id]),
        'at_client_page': True,
        'profile_image': profile_image})


def clientProfile(request, id, idclient):
    client = get_object_or_404(Freelancer, id=id)
    p = get_object_or_404(CompanyManager, id=idclient)

    if request.method == "POST":
        action = request.POST.get("action")
        comment_id = request.POST.get("comment_id")

        if action == "new_comment":
            comment_content = request.POST.get("comment")
            if comment_content:
                CommentProfile.objects.create(
                    user_profile=p,
                    author=client,
                    content=comment_content,       
                )
                messages.success(request, "Comentario publicado correctamente.")
            else:
                messages.error(request, "El comentario no puede estar vacío.")

        elif action == "edit_comment" and comment_id:
            comment = get_object_or_404(CommentProfile, id=comment_id, author=client)
            new_content = request.POST.get("new_content")
            if new_content:
                comment.content = new_content
                comment.save()
                messages.success(request, "Comentario editado correctamente.")
            else:
                messages.error(request, "El comentario editado no puede estar vacío.")

        elif action == "delete_comment" and comment_id:
            comment = get_object_or_404(CommentProfile, id=comment_id, author=client)
            comment.delete()
            messages.success(request, "Comentario eliminado correctamente.")
        
        elif action == "rate_profile":
            
            existing_rating = Rating.objects.filter(user_profile=p, author=client).first()

            if existing_rating:
                messages.error(request, "Ya has calificado a esta compañía.")
            else:
                score = float(request.POST.get("score"))
                if score:
                   
                    Rating.objects.create(
                        user_profile=p,
                        author=client,
                        score=score,
                        date_rated=datetime.now().date(),
                    )
                    
                    average_rating = Rating.objects.filter(user_profile=p).aggregate(Avg('score'))['score__avg']
                    p.rating = average_rating if average_rating else 0 
                    p.save()

                    messages.success(request, "Calificación enviada correctamente.")
                else:
                    messages.error(request, "La calificación no puede ser vacía.")

        return redirect('clientProfile', id=id, idclient=idclient)

    profile_image = client.image.url
    profile_url = reverse('perfilFreelancer', args=[client.id])
    return render(request, 'perfil/client_profile_view.html', {
        'p': p,
        'projects_url': reverse('projectsList', args=[p.id]),
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'profile_image': profile_image,
        'client': client,
        'profile_url': profile_url,
        'can_rate': True,
        'show_edit_link': False})

def freelancerProfile(request, id, idclient):
    p = get_object_or_404(Freelancer, id=id)
    client = get_object_or_404(CompanyManager, id=idclient)

    if request.method == "POST":
        action = request.POST.get("action")
        comment_id = request.POST.get("comment_id")

        if action == "new_comment":
            comment_content = request.POST.get("comment")
            if comment_content:
                CommentProfile.objects.create(
                    user_profile=p,
                    author=client,
                    content=comment_content,       
                )
                messages.success(request, "Comentario publicado correctamente.")
            else:
                messages.error(request, "El comentario no puede estar vacío.")

        elif action == "edit_comment" and comment_id:
            comment = get_object_or_404(CommentProfile, id=comment_id, author=client)
            new_content = request.POST.get("new_content")
            if new_content:
                comment.content = new_content
                comment.save()
                messages.success(request, "Comentario editado correctamente.")
            else:
                messages.error(request, "El comentario editado no puede estar vacío.")

        elif action == "delete_comment" and comment_id:
            comment = get_object_or_404(CommentProfile, id=comment_id, author=client)
            comment.delete()
            messages.success(request, "Comentario eliminado correctamente.")

        elif action == "rate_profile":
            
            existing_rating = Rating.objects.filter(user_profile=p, author=client).first()

            if existing_rating:
                messages.error(request, "Ya has calificado a este freelancer.")
            else:
                score = float(request.POST.get("score"))
                if score:
                   
                    Rating.objects.create(
                        user_profile=p,
                        author=client,
                        score=score,
                        date_rated=datetime.now().date(),
                    )
                    
                    average_rating = Rating.objects.filter(user_profile=p).aggregate(Avg('score'))['score__avg']
                    p.rating = average_rating if average_rating else 0 
                    p.save()

                    messages.success(request, "Calificación enviada correctamente.")
                else:
                    messages.error(request, "La calificación no puede ser vacía.")

        return redirect('freelancerProfile', id=id, idclient=idclient)

    profile_image = client.image.url
    profile_url = reverse('perfilesCliente', args=[client.id])
    return render(request, 'perfil/freelancer_profile_view.html', {
        'p': p,
        'profile_image': profile_image,
        'client': client,
        'profile_url': profile_url,
        'home_url': reverse('mainCliente', args=[p.id]),
        'at_client_page': True,
        'can_rate': True,
        'show_edit_link': False})

def mainFreelancer(request, id):
    profile = get_object_or_404(Freelancer, id=id)

    if profile.is_active == False:
        profile.is_active = True
        profile.save()
        messages.info(request, 'Your account was disabled, now it is enable again.')

    search_query = request.GET.get('search', '')

    projects_list = Project.objects.all()
    print(projects_list)
    if search_query:
        projects_list = projects_list.filter(name__icontains=search_query)

    category_id = request.GET.get('category')
    if category_id:
        projects_list = projects_list.filter(projectcategories__id=category_id)

    company_id = request.GET.get('company')
    if company_id:
        projects_list = projects_list.filter(clientprofile__id=company_id)

    budget_min = request.GET.get('budget_min')
    budget_max = request.GET.get('budget_max')
    if budget_min and budget_max:
        try:
            budget_min_value = float(budget_min)
            budget_max_value = float(budget_max)

            if budget_min_value <= budget_max_value:
                projects_list = projects_list.filter(
                    budget__gte=budget_min_value, 
                    budget__lte=budget_max_value
                )
        except ValueError:
            pass  

    project_type = request.GET.get('type') 
    if project_type:
        projects_list = projects_list.filter(type=project_type)

    # Configuración de paginación
    paginator = Paginator(projects_list, 12)
    page_number = request.GET.get('page')  
    projects = paginator.get_page(page_number)

    for project in projects:
        project.profile_url = reverse('freelancer_project', args=[profile.id, project.id])

    categories = ProjectCategory.objects.all()
    companies = CompanyManager.objects.filter(projects__isnull=False).distinct()

    profile_image = profile.image.url
    profile_url = reverse('perfilFreelancer', args=[profile.id])
    return render(request, 'perfil/freelancer_home.html', {
        'profile': profile,
        'projects_url': reverse('projectsList', args=[profile.id]),
        'at_home': True,
        'profile_image': profile_image,
        'profile_url': profile_url,
        'projects': projects, 
        'categories': categories,
        'companies': companies,
        'search_query': search_query,
        'budget_min': budget_min,
        'budget_max': budget_max  
    })

def mainCliente(request, id):        
    p = get_object_or_404(CompanyManager, id=id)

    if p.is_active == False:
        p.is_active = True
        p.save()
        messages.info(request, 'Your account was disabled, now it is enable again.')


    profile_image = p.image.url
    profile_url = reverse('perfilesCliente', args=[p.id])
    return render(request, 'perfil/client_projects_list.html', {
        'p':p,
        'at_home': True,
        'at_client_page': True,
        'profile_image': profile_image,
        'profile_url': profile_url})

def firstMain(request):

    publications = Project.objects.all()[:3]
    return render(request, 'perfil/home_page.html', {'publications': publications})

def projectsList(request, id):
    p = get_object_or_404(Freelancer, id=id)

    projects = Project.objects.filter(milestones__freelancer=p).distinct()

    profile_image = p.image.url
    profile_url = reverse('perfilFreelancer', args=[p.id])
    return render(request, 'perfil/freelancer_projects_list.html', {
        'profile': p,
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'at_projects_page': True,
        'profile_image': profile_image,
        'profile_url': profile_url,
        'projects': projects
    })

def manageProject(request, id, id_project):
    p = get_object_or_404(CompanyManager, id=id)
    pr = get_object_or_404(Project, id=id_project)

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "accept_application":
            application_id = request.POST.get("application_id")
            application = get_object_or_404(Application, id=application_id)
            milestone = application.milestone
            if milestone.freelancer is None:
                application.state = 'Approved'
                freelancer = get_object_or_404(Freelancer, id=application.freelancer.id)
                milestone.freelancer = freelancer

                for task in milestone.tasks.all():
                    task.freelancer = freelancer
                    task.save()

                application.save()
                milestone.save()
                #Notificar al freelancer
                messages.success(request, "Solicitud aprovada y notificada al freelancer.")
            else:
                messages.error(request, "El milestone al que aplicó el freelancer ya fue asignado. No puede aceptar la solicitud.")

        elif action == "reject_application":
            application_id = request.POST.get("application_id")
            application = get_object_or_404(Application, id=application_id)
            application.state = 'Rejected'
            application.save()
            #Notificar al freelancer
            messages.success(request, "Solicitud rechazada y notificada al freelancer.")
        
        elif action == "send_assignment_comment":
            assignment_id = request.POST.get("assignment_id")
            comment = request.POST.get("assigment_comment")
            assignment = get_object_or_404(Assignment, id=assignment_id)
            assignment.manager_comment = comment
            assignment.checked = True
            assignment.save()
            #Notificar al freelancer
            messages.success(request, "Comentario enviado al freelancer exitosamente.")
        
        elif action == "make_payment":
            milestone_id = request.POST.get("milestone")
            milestone = get_object_or_404(Milestone, id=milestone_id)
            milestone.paid = True
            milestone.save()

            currency = request.POST.get("currency")
            amount = request.POST.get("amount")
            freelancer_id = request.POST.get("freelancer")
            freelancer = get_object_or_404(Freelancer, id=freelancer_id)
            freelancer_name = freelancer.name
            #Notificar al freelancer
            messages.success(request, f"{amount} {currency} enviados a {freelancer_name} exitosamente.")

        return redirect('manageProject', id, id_project)

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
                'paid': milestone.paid,
                'name': milestone.name,
                'progress1': milestone.progress,
                'start_date': milestone.start_date.strftime('%Y-%m-%d'),
                'end_date': milestone.end_date.strftime('%Y-%m-%d'),
                'tasks': [
                    {
                        'name': task.name,
                        'state': task.state
                    }
                    for task in milestone.tasks.all()
                ],
                'freelancer': {
                    'id': milestone.freelancer.id,
                    'name': milestone.freelancer.name if milestone.freelancer else None,
                    'profile_picture': milestone.freelancer.image.url if milestone.freelancer and milestone.freelancer.image else None,
                } if milestone.freelancer else None,
                'applications': [
                    {
                        'id': application.id,
                        'state': application.state,
                        'freelancer_id': application.freelancer.id,
                        'freelancer_name': application.freelancer.name,
                        'freelancer_picture': application.freelancer.image.url if application.freelancer.image else None,
                    }
                    for application in milestone.applications.all()
                ]
            }
            for milestone in pr.milestones.all()
        ],
        'assignments': [
            {
                'id': assignment.id,
                'name': assignment.name,
                'task': assignment.task.name,
                'milestone_id': assignment.task.milestone.id,
                'freelancer': assignment.task.freelancer.name,
                'date': assignment.date.strftime('%Y-%m-%d'), 
                'checked': assignment.checked,
                'file': assignment.file.url if assignment.file else None,
                'url': assignment.url
            }
            for assignment in pr.assignments.all()
        ]
    }

    profile_image = p.image.url
    profile_url = reverse('perfilesCliente', args=[p.id])
    return render(request, 'perfil/client_project_view.html', {
        'profile': p,
        'project_progress': project_progress,
        'project': project_data,
        'home_url': reverse('mainCliente', args=[p.id]),
        'at_client_page': True,
        'profile_image': profile_image,
        'profile_url': profile_url,
    })

def projectWorkspace(request, id, id_project):
    p = get_object_or_404(Freelancer, id=id)
    pr = get_object_or_404(Project, id=id_project)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_tasks":
            milestone_id = request.POST.get("milestones-select")
            if milestone_id:
                milestone = get_object_or_404(Milestone, id=milestone_id)
                for task in milestone.tasks.all():
                    task_state = request.POST.get(f'task_{task.id}')
                    if task_state:
                        task.state = task_state
                        task.save()
                
                milestone.calculate_progress()
                messages.success(request, f"Estado de las tareas del milestone '{milestone.name}' actualizado exitosamente.")

        elif action == "send_assignment":
            task_id = request.POST.get("task-select")
            task = get_object_or_404(Task, id=task_id)
            milestone_id = task.milestone.id
            milestone = get_object_or_404(Task, id=milestone_id)
            name = request.POST.get("name")
            link = request.POST.get("link")
            file = request.FILES.get("assignment-file")
            Assignment.objects.create(
                project=pr,
                name=name,
                task=task,
                file=file,
                url=link
            )
            messages.success(request, "Entregable enviado exitosamente.")

        return redirect('projectWorkspace', id=id, id_project=id_project)

    project_data = {
        'id': pr.id,
        'name': pr.name,
        'milestones': [
            {
                'id': milestone.id,
                'name': milestone.name,
                'tasks': [
                    {
                        'id': task.id,
                        'name': task.name,
                        'deadline': task.deadline.strftime('%Y-%m-%d'),
                        'state': task.state,
                        'description': task.description
                    }
                    for task in milestone.tasks.filter(freelancer=p) 
                ]
            }
            for milestone in pr.milestones.filter(freelancer=p)
        ],
        'assignments': [
            {
                'name': assignment.name,
                'task': assignment.task.name,
                'date': assignment.date,
                'checked': assignment.checked,
                'file': assignment.file.url if assignment.file else None,
                'url': assignment.url,
                'comment': assignment.manager_comment
            }
            for assignment in pr.assignments.filter(task__freelancer=p)
        ]
    }

    profile_url = reverse('perfilFreelancer', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/freelancer_project_workspace.html', {
        'profile': p,
        'projects_url': reverse('projectsList', args=[p.id]),
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'profile_url': profile_url,
        'profile_image': profile_image,
        'project': project_data,  
    })


def deleteDisable(request, id=id):
    p = get_object_or_404(Freelancer, id=id)

    if request.method == "POST":
        user = get_object_or_404(User, id=p.id)
        action = request.POST.get("action")
        if action == "delete":
            user.delete()
            return redirect('home', id="accountDeleted")
        
        elif action == "disable":
            user.is_active = False
            user.save()
            return redirect('home', id="accountDisabled")
        
    profile_url = reverse('perfilFreelancer', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/freelancer_edit_profile_delete.html', {
        'p': p,
        'profile_image': profile_image,
        'projects_url': reverse('projectsList', args=[p.id]),
        'home_url': reverse('mainFreelancer', args=[p.id]),
        'profile_url': profile_url})

def deleteDisableClient(request, id=id):
    p = get_object_or_404(CompanyManager, id=id)

    if request.method == "POST":
        user = get_object_or_404(User, id=p.id)
        action = request.POST.get("action")
        if action == "delete":
            user.delete()
            return redirect('home', id="accountDeleted")
        
        elif action == "disable":
            user.is_active = False
            user.save()
            return redirect('home', id="accountDisabled")

    profile_url = reverse('perfilesCliente', args=[p.id])
    profile_image = p.image.url
    return render(request, 'perfil/client_edit_profile_delete.html', {
        'p': p,
        'profile_image': profile_image,
        'home_url': reverse('mainCliente', args=[p.id]),
        'at_client_page': True,
        'profile_url': profile_url})

def calendar(request):
    return render(request, 'perfil/calendar.html')



