from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
import json
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
#from .forms import CompanyRegistrationForm, FreelancerRegistrationForm, LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password, check_password

from my_aplication.models import Freelancer, CompanyManager, User
from .forms import createProjectForm, editProjectForm
import os

from my_aplication.models import Freelancer, CompanyManager, Project, Milestone, Task

#SMTP libraries
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from marketplace.settings import EMAIL_HOST_USER

countries = [' Afganistán',' Albania',' Alemania',' Andorra',' Angola',' Antigua y Barbuda',' Arabia Saudita',' Argelia',' Argentina',' Armenia',' Australia',' Austria',' Azerbaiyán',' Bahamas',' Bangladés',' Barbados',' Baréin',' Bélgica',' Belice',' Benín',' Bielorrusia',' Birmania',' Bolivia',' Bosnia y Herzegovina',' Botsuana',' Brasil',' Brunéi',' Bulgaria',' Burkina Faso',' Burundi',' Bután',' Cabo Verde',' Camboya',' Camerún',' Canadá',' Catar',' Chad',' Chile',' China',' Chipre',' Ciudad del Vaticano',' Colombia',' Comoras',' Corea del Norte',' Corea del Sur',' Costa de Marfil',' Costa Rica',' Croacia',' Cuba',' Dinamarca',' Dominica',' Ecuador',' Egipto',' El Salvador',' Emiratos Árabes Unidos',' Eritrea',' Eslovaquia',' Eslovenia',' España',' Estados Unidos',' Estonia',' Etiopía',' Filipinas',' Finlandia',' Fiyi',' Francia',' Gabón',' Gambia',' Georgia',' Ghana',' Granada',' Grecia',' Guatemala',' Guyana',' Guinea',' Guinea ecuatorial',' Guinea-Bisáu',' Haití',' Honduras',' Hungría',' India',' Indonesia',' Irak',' Irán',' Irlanda',' Islandia',' Islas Marshall',' Islas Salomón',' Israel',' Italia',' Jamaica',' Japón',' Jordania',' Kazajistán',' Kenia',' Kirguistán',' Kiribati',' Kuwait',' Laos',' Lesoto',' Letonia',' Líbano',' Liberia',' Libia',' Liechtenstein',' Lituania',' Luxemburgo',' Madagascar',' Malasia',' Malaui',' Maldivas',' Malí',' Malta',' Marruecos',' Mauricio',' Mauritania',' México',' Micronesia',' Moldavia',' Mónaco',' Mongolia',' Montenegro',' Mozambique',' Namibia',' Nauru',' Nepal',' Nicaragua',' Níger',' Nigeria',' Noruega',' Nueva Zelanda',' Omán',' Países Bajos',' Pakistán',' Palaos',' Panamá',' Papúa Nueva Guinea',' Paraguay',' Perú',' Polonia',' Portugal',' Reino Unido',' República Centroafricana',' República Checa',' República de Macedonia',' República del Congo',' República Democrática del Congo',' República Dominicana',' República Sudafricana',' Ruanda',' Rumanía',' Rusia',' Samoa',' San Cristóbal y Nieves',' San Marino','San Vicente y las Granadinas',' Santa Lucía',' Santo Tomé y Príncipe',' Senegal',' Serbia',' Seychelles',' Sierra Leona',' Singapur',' Siria',' Somalia',' Sri Lanka',' Suazilandia',' Sudán',' Sudán del Sur',' Suecia',' Suiza',' Surinam',' Tailandia',' Tanzania',' Tayikistán',' Timor Oriental',' Togo',' Tonga',' Trinidad y Tobago',' Túnez',' Turkmenistán',' Turquía',' Tuvalu',' Ucrania',' Uganda',' Uruguay',' Uzbekistán',' Vanuatu',' Venezuela',' Vietnam',' Yemen',' Yibuti',' Zambia',' Zimbabue']

def login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

            if check_password(password, user.password):

                auth_login(request, user)

                if Freelancer.objects.filter(id=user.id).exists():
                    return redirect('mainFreelancer', id=user.id) 
                elif CompanyManager.objects.filter(id=user.id).exists():
                    return redirect('mainCliente', id=user.id) 
                else:
                    return redirect('home') 

            else:
                return render(request, 'login.html', {'incorrect_credentials': True})
        
        except User.DoesNotExist:
            return render(request, 'login.html', {'incorrect_credentials': True})

    return render(request, 'login.html')


def recover(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        #enviar mensaje por correo usando SMTP y el email
        send_recovery_email(email, 'prueba123')

        return redirect('recover_confirmation')
    else:
        return render(request, 'PasswordRecovery.html')

def recover_confirmation(request):
    return render(request, 'PasswordRecoveryConfirmation.html')

def send_recovery_email(email, password):
    message = "Dear user, in response to your request, we are sending you your password: " + password
    send_mail('Recover your password!',message,EMAIL_HOST_USER,[email],fail_silently=False)

#Registro de Freelancers
def registerf1(request):

    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.POST.get('username')
        name = request.POST.get('fullname')
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Comprobar si el nombre de usuario ya existe
        if email and User.objects.filter(username=email).exists():
            return render(request, 'signUp1.html', {'username_exists': True})

        freelancer = Freelancer.objects.create(
            username=email,
            password=make_password(password),
            name=name,
            phone=phone
        )

        return redirect('registerf2', id=freelancer.id)  # Redirigir al siguiente paso con el ID del freelancer

    else:
        return render(request, 'signUp1.html', {'username_exists': False, 'email_exists': False})


    
def registerf2(request, id):
    if request.method == 'POST':
        if 'image_input' not in request.FILES:
            return redirect('registerf3', id = id)
        else:
            image = request.FILES.get('image_input')
            if image:
                freelancer_profile = Freelancer.objects.get(id=id)
                freelancer_profile.image = image
                freelancer_profile.save()
            return redirect('registerf3', id = id)
    else:
        return render(request, 'singup2.html', {'id': id})

def registerf3(request, id):
    if request.method == 'POST':
        freelancer = Freelancer.objects.get(id=id)
        country = request.POST.get('country')
        identification = request.POST.get('identification')

        freelancer.country = country
        freelancer.identification = identification
        freelancer.save()
        return redirect('login')
    else:
        return render(request, 'SignUp3.html', {'countries': countries})

#Registro de Company
def registerc1(request):
    username = request.POST.get('username')
    object = User.objects.filter(username=username)
    if request.method == 'POST':
        #verificacion del usuario (que no exista)
        if object.exists():
            #devolver alerta tipo js
            return render(request, 'signUp1Company.html', {'username_exists': True})
        else:
            username = request.POST.get('username')
            company_name = request.POST.get('name')
            legal_agent = request.POST.get('legal_agent')
            password = request.POST.get('password')

            company = CompanyManager.objects.create(
                username = username,
                name = company_name,
                phone=None,
                password = make_password(password),
                country=None,
                address=None,
                legal_agent=legal_agent,
                business_vertical=None,
                company_type=None)
            return redirect('registerc2', id = company.id)
    else:
        return render(request, 'signUp1Company.html', {'username_exists': False})
    
def registerc2(request, id):
    if request.method == 'POST':
        user = CompanyManager.objects.get(id=id)
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        business_vertical = request.POST.get('business_vertical')
        company_type = request.POST.get('company_type')
        user.country = country
        user.phone = phone
        user.address = address
        user.business_vertical = business_vertical
        user.company_type = company_type
        user.save()
        return redirect('login')
    else:
        return render(request, 'signUp2Company.html', {'countries': countries})
    
def addproject(request):
    return render(request, 'AddProject.html')

def editproject(request):
    return render(request, 'EditProject.html')

def create_project_view(request, id):
    client = CompanyManager.objects.get(id=id)

    context = {
        'profile_image': client.image.url,
        'home_url': reverse('mainCliente', args=[client.id]),
        'profile_url': reverse('perfilesCliente', args=[client.id]),
        'at_client_page': True,
        'company_manager': client
    }
    return render(request, 'AddProject.html', context)

def edit_project_view(request, id_client, id_project):
    project = Project.objects.get(id=id_project)
    milestones = project.milestones.all()
    client = CompanyManager.objects.get(id=id_client)
    
    context = {
        'project': project,
        'milestones': milestones,
        'profile_image': client.image.url,
        'home_url': reverse('mainCliente', args=[client.id]),
        'profile_url': reverse('perfilesCliente', args=[client.id]),
        'at_client_page': True
    }
    return render(request, 'EditProject.html', context)

@csrf_exempt
def post_project(request):
    if request.method == 'POST':
        manager_id = request.POST.get('manager')
        print(f"Manager ID: {manager_id}")
        name = request.POST.get('name')
        description = request.POST.get('description')
        budget = request.POST.get('budget')
        project_picture = request.FILES.get('project_picture')
        if project_picture:

            project = Project.objects.create(
                manager_id=manager_id,
                name=name,
                description=description,
                budget=budget,
                project_picture=project_picture
            )
        else:
            project = Project.objects.create(
                manager_id=manager_id,
                name=name,
                description=description,
                budget=budget
            )

        # form = createProjectForm(request.POST, request.FILES)

        milestones_json =  request.POST.get('milestones')
        if milestones_json:
            milestones = json.loads(milestones_json)

            for milestone_data in milestones:
                milestone = Milestone.objects.create(
                    name=milestone_data['name'],
                    description=milestone_data['description'],
                    end_date=milestone_data['deadline'],
                    project=project
                )
                
                tasks = milestone_data.get('tasks', [])
                for task_data in tasks:
                    Task.objects.create(
                        name=task_data['name'],
                        milestone=milestone,
                    )

            return JsonResponse({'success': True, 'message': 'Project created successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': 'Something happened with the milestones'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def post_project_edition(request, id=None):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=id)
        
        # Update the project fields
        project.name = request.POST.get('name', project.name)
        project.description = request.POST.get('description', project.description)
        project.budget = request.POST.get('budget', project.budget)
        
        # Handle project picture update if provided
        project_picture = request.FILES.get('project_picture')
        if project_picture:
            # Delete the old picture if a new one is uploaded
            if project.project_picture:
                old_picture_path = project.project_picture.path
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)

            # Assign the new picture
            project.project_picture = project_picture
        
        project.save()  # Save the project updates

        deleted_milestones = json.loads(request.POST.get('deletedMilestones', '[]'))
        deleted_tasks = json.loads(request.POST.get('deletedTasks', '[]'))

        # Delete specified milestones
        if deleted_milestones:
            Milestone.objects.filter(id__in=deleted_milestones, project=project).delete()

        # Delete specified tasks
        if deleted_tasks:
            Task.objects.filter(id__in=deleted_tasks, milestone__project=project).delete()
        
        milestones_json = request.POST.get('milestones')
        if milestones_json:
            milestones = json.loads(milestones_json)

            for milestone_data in milestones:
                # Check if the milestone already exists and update it, or create a new one
                milestone_id = milestone_data.get('id')
                if milestone_id:
                    milestone = Milestone.objects.filter(id=milestone_id, project=project).first()
                    if milestone:
                        milestone.name = milestone_data['name']
                        milestone.description = milestone_data['description']
                        milestone.end_date = milestone_data['deadline']
                        milestone.save()
                else:
                    # Create a new milestone if no ID is provided
                    milestone = Milestone.objects.create(
                        name=milestone_data['name'],
                        description=milestone_data['description'],
                        end_date=milestone_data['deadline'],
                        project=project
                    )
                
                # Handle tasks within the milestone
                tasks = milestone_data.get('tasks', [])
                for task_data in tasks:
                    task_id = task_data.get('id')
                    if task_id:
                        task = Task.objects.filter(id=task_id, milestone=milestone).first()
                        if task:
                            task.name = task_data['name']
                            task.save()
                    else:
                        # Create a new task if no ID is provided
                        Task.objects.create(
                            name=task_data['name'],
                            milestone=milestone,
                        )

            return JsonResponse({'success': True, 'message': 'Project edited successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'No milestones data provided'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})



