from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from .forms import CompanyRegistrationForm, FreelancerRegistrationForm, LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password

from my_aplication.models import Freelancer, CompanyManager, User

#SMTP libraries
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from marketplace.settings import EMAIL_HOST_USER

countries = [' Afganistán',' Albania',' Alemania',' Andorra',' Angola',' Antigua y Barbuda',' Arabia Saudita',' Argelia',' Argentina',' Armenia',' Australia',' Austria',' Azerbaiyán',' Bahamas',' Bangladés',' Barbados',' Baréin',' Bélgica',' Belice',' Benín',' Bielorrusia',' Birmania',' Bolivia',' Bosnia y Herzegovina',' Botsuana',' Brasil',' Brunéi',' Bulgaria',' Burkina Faso',' Burundi',' Bután',' Cabo Verde',' Camboya',' Camerún',' Canadá',' Catar',' Chad',' Chile',' China',' Chipre',' Ciudad del Vaticano',' Colombia',' Comoras',' Corea del Norte',' Corea del Sur',' Costa de Marfil',' Costa Rica',' Croacia',' Cuba',' Dinamarca',' Dominica',' Ecuador',' Egipto',' El Salvador',' Emiratos Árabes Unidos',' Eritrea',' Eslovaquia',' Eslovenia',' España',' Estados Unidos',' Estonia',' Etiopía',' Filipinas',' Finlandia',' Fiyi',' Francia',' Gabón',' Gambia',' Georgia',' Ghana',' Granada',' Grecia',' Guatemala',' Guyana',' Guinea',' Guinea ecuatorial',' Guinea-Bisáu',' Haití',' Honduras',' Hungría',' India',' Indonesia',' Irak',' Irán',' Irlanda',' Islandia',' Islas Marshall',' Islas Salomón',' Israel',' Italia',' Jamaica',' Japón',' Jordania',' Kazajistán',' Kenia',' Kirguistán',' Kiribati',' Kuwait',' Laos',' Lesoto',' Letonia',' Líbano',' Liberia',' Libia',' Liechtenstein',' Lituania',' Luxemburgo',' Madagascar',' Malasia',' Malaui',' Maldivas',' Malí',' Malta',' Marruecos',' Mauricio',' Mauritania',' México',' Micronesia',' Moldavia',' Mónaco',' Mongolia',' Montenegro',' Mozambique',' Namibia',' Nauru',' Nepal',' Nicaragua',' Níger',' Nigeria',' Noruega',' Nueva Zelanda',' Omán',' Países Bajos',' Pakistán',' Palaos',' Panamá',' Papúa Nueva Guinea',' Paraguay',' Perú',' Polonia',' Portugal',' Reino Unido',' República Centroafricana',' República Checa',' República de Macedonia',' República del Congo',' República Democrática del Congo',' República Dominicana',' República Sudafricana',' Ruanda',' Rumanía',' Rusia',' Samoa',' San Cristóbal y Nieves',' San Marino','San Vicente y las Granadinas',' Santa Lucía',' Santo Tomé y Príncipe',' Senegal',' Serbia',' Seychelles',' Sierra Leona',' Singapur',' Siria',' Somalia',' Sri Lanka',' Suazilandia',' Sudán',' Sudán del Sur',' Suecia',' Suiza',' Surinam',' Tailandia',' Tanzania',' Tayikistán',' Timor Oriental',' Togo',' Tonga',' Trinidad y Tobago',' Túnez',' Turkmenistán',' Turquía',' Tuvalu',' Ucrania',' Uganda',' Uruguay',' Uzbekistán',' Vanuatu',' Venezuela',' Vietnam',' Yemen',' Yibuti',' Zambia',' Zimbabue']

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Realizar la autenticación
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Iniciar sesión

            # Verificar si el usuario es un Freelancer o un CompanyManager
            if Freelancer.objects.filter(id=user.id).exists():
                return redirect('mainFreelancer', id=user.id)  # Redirigir a la vista de Freelancer
            elif CompanyManager.objects.filter(id=user.id).exists():
                return redirect('mainCompany', id=user.id)  # Redirigir a la vista de CompanyManager
            else:
                return redirect('home')  # Redirigir a una vista predeterminada si no es Freelancer ni CompanyManager

        else:
            # En caso de error en la autenticación, volver a mostrar el formulario con un mensaje de error
            return render(request, 'login.html', {'incorrect_credentials': True})

    # Si el método de la solicitud no es POST, simplemente muestra el formulario de inicio de sesión
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
        username = request.POST.get('username')
        name = request.POST.get('fullname')
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Comprobar si el valor es un correo electrónico
        if '@' in username:
            email = username
            username = email
        else:
            email = None
            username = username

        # Comprobar si el nombre de usuario ya existe
        if username and User.objects.filter(username=username).exists():
            print('hehehhehe')
            return render(request, 'signUp1.html', {'username_exists': True})

        freelancer = Freelancer.objects.create(
            username=username,
            email=email,
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
        identification = request.POST.get('identification')
        freelancer_profile.country = country
        freelancer_profile.identification = identification
        freelancer_profile.save()
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
    return render(request, 'EditProject.html')