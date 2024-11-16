import json
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
#from .forms import CompanyRegistrationForm, FreelancerRegistrationForm, LoginForm
from django.contrib.auth.views import LoginView
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
        #realizar la autenticacion, que se quede logeado toda la app
        user = authenticate(request, username=username, password=password)
        return redirect('home')#cambiar a dashboard
    else:
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
        #verificacion del usuario (que no exista)
        username = request.POST.get('username')
        object = Freelancer.objects.filter(username=username)
        if object.exists():
            #devolver alerta tipo js
            return render(request, 'signUp1.html', {'username_exists': True})
        else:
            username = request.POST.get('username')
            fullname = request.POST.get('fullname')
            print('name:', fullname)
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password')

            freelancer_profile = Freelancer.objects.create(name=fullname, email=username, phone=phone_number, image=None)
            user = Freelancer.objects.create(username=username, password=password, profile=freelancer_profile)
            return redirect('registerf2', id = user.profile.id)
    else:
        return render(request, 'signUp1.html', {'username_exists': False})
    
def registerf2(request, id):
    if request.method == 'POST':
        if 'image_input' not in request.FILES:
            return redirect('registerf3', id = id)
        else:
            image = request.FILES.get('image_input')
            freelancer_profile = Freelancer.objects.get(id=id)
            freelancer_profile.image = image
            freelancer_profile.save()
            return redirect('registerf3', id = id)
    else:
        return render(request, 'singup2.html', {'id': id})

def registerf3(request, id):
    if request.method == 'POST':
        freelancer_profile = Freelancer.objects.get(id=id)
        country = request.POST.get('country')
        user = Freelancer.objects.get(profile=freelancer_profile)
        user.country = country
        user.identification = id
        user.save()
        return redirect('login')
    else:
        return render(request, 'SignUp3.html', {'countries': countries})

#Registro de Company
def registerc1(request):
    username = request.POST.get('username')
    object = CompanyManager.objects.filter(username=username)
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

            company_profile = CompanyManager.objects.create(name=company_name, email=username, phone=None, image=None, address=None, legal_agent=legal_agent, business_vertical=None, company_type=None)
            user = CompanyManager.objects.create(username=username, password=password, profile=company_profile)
            return redirect('registerc2', id = user.profile.id)
    else:
        return render(request, 'signUp1Company.html', {'username_exists': False})
    
def registerc2(request, id):
    if request.method == 'POST':
        company_profile = CompanyManager.objects.get(id=id)
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        business_vertical = request.POST.get('business_vertical')
        company_type = request.POST.get('company_type')
        user = CompanyManager.objects.get(profile=company_profile)
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
    company_manager = CompanyManager.objects.get(id=id)
    return render(request, 'AddProject.html', {'company_manager': company_manager})

def edit_project_view(request, id):
    project = Project.objects.get(id=id)
    milestones = project.milestones.all()
    
    context = {
        'project': project,
        'milestones': milestones
    }
    return render(request, 'EditProject.html', context)

@csrf_exempt
def post_project(request):
    if request.method == 'POST':
        manager_id = request.POST.get('manager')
        name = request.POST.get('name')
        description = request.POST.get('description')
        budget = request.POST.get('budget')
        project_picture = request.FILES.get('project_picture')

        project = Project.objects.create(
            manager_id=manager_id,
            name=name,
            description=description,
            budget=budget,
            project_picture=project_picture
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



