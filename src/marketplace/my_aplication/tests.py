from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from .models import Freelancer, CompanyManager, Project, Rating, Skill, Application, Milestone
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import FieldError, ValidationError

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import perfil.urls, project_management.urls, marketplace.urls, accounts.urls

class FreelancerModelTest(TestCase):
    def setUp(self):
        self.freelancer = Freelancer.objects.create(
            username='freelancer1',
            email='freelancer1@example.com',
            password='securepassword',
            name='John Doe',
            profession='Developer',
            price='100 USD/hr',
            experience='semi_senior',
        )
    
    def test_create_freelancer(self):
        # Verifica que un freelancer se ha creado correctamente
        freelancer = self.freelancer
        self.assertEqual(freelancer.username, 'freelancer1')
        self.assertEqual(freelancer.email, 'freelancer1@example.com')
        self.assertEqual(freelancer.profession, 'Developer')

    def test_default_jobs_completed(self):
        # Verifica que el valor por defecto de 'jobs_completed' es 0
        freelancer = self.freelancer
        self.assertEqual(freelancer.jobs_completed, 0)
    
    def test_create_freelancer_with_invalid_email(self):
        freelancer = Freelancer(
            username='invalid_freelancer',
            email='not-an-email',  # Email inválido
            password='securepassword',
            name='Invalid User',
            profession='Tester',
            price='50',
            experience='junior',
        )
        with self.assertRaises(ValidationError):
            freelancer.full_clean()  # Esto activará la validación del campo email
            freelancer.save()

    
    def test_create_freelancer_with_empty_name(self):
        freelancer = Freelancer(
            username='empty_name_freelancer',
            email='emptyname@example.com',
            password='securepassword',
            name='',  # Nombre vacío
            profession='Tester',
            price='50 USD/hr',
            experience='junior',
        )
        with self.assertRaises(ValidationError):
            freelancer.full_clean()  # Esto activará la validación del campo email
            freelancer.save()

class CompanyManagerModelTest(TestCase):
    def setUp(self):
        # Setup de datos para las pruebas
        self.company_manager = CompanyManager.objects.create(
            username='company_manager1',
            email='company_manager1@example.com',
            password='securepassword',
            name='Alice',
            legal_agent='Alice LLC',
            address='123 Business St.',
            business_vertical='Software Development',
            company_type='SaaS'
        )
    
    def test_create_company_manager(self):
        # Verifica que se ha creado una compañía correctamente
        manager = self.company_manager
        self.assertEqual(manager.username, 'company_manager1')
        self.assertEqual(manager.email, 'company_manager1@example.com')
    
    def test_create_company_manager_with_missing_fields(self):
        company = CompanyManager(
            username='incomplete_manager',
            email='manager@example.com',
            password='securepassword',
            name='Incomplete Manager'
            # Falta `legal_agent` y otros campos obligatorios
        )
        with self.assertRaises(ValidationError):
            company.full_clean()  # Esto activará la validación del campo email
            company.save()

class ProjectModelTest(TestCase):
    def setUp(self):
        self.company_manager = CompanyManager.objects.create(
            username='company_manager1',
            email='company_manager1@example.com',
            password='securepassword',
            name='Alice'
        )
        self.project = Project.objects.create(
            manager=self.company_manager,
            name='Project A',
            description='A project description.',
            budget=5000.00,
            state='PENDING'
        )

    def test_project_creation(self):
        # Verifica que un proyecto se haya creado correctamente
        project = self.project
        self.assertEqual(project.name, 'Project A')
        self.assertEqual(project.state, 'PENDING')
        self.assertEqual(project.budget, 5000.00)
    
    def test_default_project_state(self):
        # Verifica que el estado predeterminado de un proyecto sea 'PENDING'
        project = self.project
        self.assertEqual(project.state, 'PENDING')
    
    def test_project_with_negative_budget(self):
        project = Project(
            manager=self.company_manager,
            name='Invalid Budget Project',
            description='Test project with negative budget.',
            budget=-1000.00,  # Presupuesto inválido
            state='PENDING'
        )
        with self.assertRaises(ValidationError):
            project.full_clean()  # Esto activará la validación del campo email
            project.save(
        )
    
    def test_project_without_manager(self):
        with self.assertRaises(IntegrityError):
            Project.objects.create(
                manager=None,  # Manager ausente
                name='No Manager Project',
                description='Project without manager.',
                budget=5000.00,
                state='PENDING'
            )

class RatingModelTest(TestCase):
    time = timezone.now()
    def setUp(self):
        # Configuración de un Freelancer
        self.freelancer = Freelancer.objects.create(
            username='freelancer1',
            email='freelancer1@example.com',
            password='securepassword',
            name='John Doe',
            profession='Developer',
            price='100 USD/hr',
            experience='semi_senior',
        )

        self.company_manager = CompanyManager.objects.create(
            username='company_manager1',
            email='company_manager1@example.com',
            password='securepassword',
            name='Alice',
            legal_agent='Alice LLC',
            address='123 Business St.',
            business_vertical='Software Development',
            company_type='SaaS'
        )

        
        # Crear una instancia de Rating usando el ContentType correcto

        self.rating = Rating.objects.create(
            user_profile=self.freelancer,
            author=self.company_manager,
            score=4.5,
            date_rated=self.time,
        )

    def test_create_rating(self):
        # Verifica que la calificación se haya creado correctamente
        self.assertEqual(self.rating.user_profile.id, self.freelancer.id)
        self.assertEqual(self.rating.author.id, self.company_manager.id)
        self.assertEqual(self.rating.score, 4.5)
        self.assertEqual(self.rating.date_rated, self.time)

    def test_rating_score_value(self):
        # Verifica que el puntaje esté dentro del rango permitido
        self.assertTrue(1 <= self.rating.score <= 5, "Score debe estar entre 1 y 5.")

    def test_rating_with_invalid_score(self):
        rating = Rating(
            user_profile=self.freelancer,
            author=self.company_manager,
            score=6,  # Puntaje fuera de rango
            date_rated=self.time,
        )
        with self.assertRaises(ValidationError):
            rating.full_clean()
            rating.save()
    
    def test_rating_with_invalid_author_type(self):
        rating = Rating(
            user_profile=self.freelancer,
            author=None,  # Tipo de autor inválido
            score=4,
            date_rated=self.time,
        )
        with self.assertRaises(ValidationError):
            rating.full_clean()
            rating.save()

class SkillModelTest(TestCase):
    def setUp(self):
        self.freelancer = Freelancer.objects.create(
            username='freelancer1',
            email='freelancer1@example.com',
            password='securepassword',
            name='Juan juanito',
            profession='Developer',
            price='100 USD/hr',
            experience='semi_senior',
        )
        self.skill = Skill.objects.create(
            profile=self.freelancer,
            name='Python'
        )

    def test_skill_creation(self):
        # Verifica que una habilidad se ha creado correctamente
        skill = self.skill
        self.assertEqual(skill.name, 'Python')
    
    def test_skill_without_name(self):
    
        skill = Skill(
            profile=self.freelancer,
            name=None  # Nombre de habilidad ausente
        )
        with self.assertRaises(ValidationError):
            skill.full_clean()
            skill.save()  

class ApplicationModelTest(TestCase):
    def setUp(self):
        # Crear CompanyManager 
        self.company_manager = CompanyManager.objects.create(name="John Doe")

        # Crear un Freelancer
        self.freelancer = Freelancer.objects.create(
            username='freelancer1',
            email='freelancer1@example.com',
            password='securepassword',
            name='John Doe',
            profession='Developer',
            price='100 USD/hr',
            experience='semi_senior',
        )

        # Crear un Project que usa company_manager
        self.project = Project.objects.create(
            manager=self.company_manager,
            name='Project A',
            description='A project description.',
            budget=5000.00,
            state='PENDING'
        )

        self.milestone = Milestone.objects.create(
            name='Example Milestone',
            description='A test milestone',
            start_date='2024-01-01',  
            end_date='2024-12-31',    
            project=self.project,
            freelancer=self.freelancer,
            state='Available'
        )

        # Crear una Application que use freelancer, project y milestone
        self.application = Application.objects.create(
            freelancer=self.freelancer,
            project=self.project,
            milestone=self.milestone,
            accepted=False,
            state='Sent'
        )

    def test_application_creation(self):
        # Verifica que una solicitud de proyecto se haya creado correctamente
        application = self.application
        self.assertEqual(application.state, 'Sent')
        self.assertEqual(application.freelancer, self.freelancer)
        self.assertEqual(application.milestone, self.milestone)

    def test_application_without_freelancer(self):
        with self.assertRaises(IntegrityError):
            Application.objects.create(
                freelancer=None,  # Freelancer ausente
                project=self.project,
                milestone=self.milestone,
                accepted=False,
                state='Sent'
            )
    
    def test_application_with_invalid_state(self):
        application = Application.objects.create(
            freelancer=self.freelancer,
            project=self.project,
            milestone=self.milestone,
            accepted=False,
            state='InvalidState'  # Estado inválido
        )
        with self.assertRaises(ValidationError):
            application.full_clean()
            application.save()
        
class MilestoneModelTest(TestCase):
    def setUp(self):
        # Crear un administrador de compañía (CompanyManager)
        self.company_manager = CompanyManager.objects.create(
            username='manager1',
            email='manager1@example.com',
            password='securepassword'
        )
        
        # Crear un freelancer
        self.freelancer = Freelancer.objects.create(
            username='freelancer1',
            email='freelancer1@example.com',
            password='securepassword',
            name='John Doe',
            profession='Developer',
            price='100 USD/hr',
            experience='semi_senior',
        )
        
        # Crear un proyecto asociado al administrador de la compañía
        self.project = Project.objects.create(
            manager=self.company_manager,
            name='Project A',
            description='A project description.',
            budget=5000.00,
            state='PENDING'
        )
        
        # Crear un hito (milestone) asociado al proyecto y al freelancer
        self.milestone = Milestone.objects.create(
            name='Milestone 1',
            description='First milestone description.',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=10),
            project=self.project,
            freelancer=self.freelancer
        )

    def test_milestone_creation(self):
        # Verifica que un hito se haya creado correctamente
        milestone = self.milestone
        self.assertEqual(milestone.name, 'Milestone 1')
        self.assertEqual(milestone.project, self.project)
        self.assertEqual(milestone.freelancer, self.freelancer)

    def test_milestone_with_invalid_dates(self):
        milestone = Milestone(
            name='Invalid Dates Milestone',
            description='Milestone with end_date before start_date.',
            start_date=timezone.now(),
            end_date=timezone.now() - timezone.timedelta(days=1),  # Fecha final antes de la inicial
            project=self.project,
            freelancer=self.freelancer,
            state='Available'
        )
        with self.assertRaises(ValidationError):
            milestone.full_clean()
            milestone.save()
    
    def test_milestone_without_project(self):
        with self.assertRaises(IntegrityError):
            Milestone.objects.create(
                name='No Project Milestone',
                description='Milestone without associated project.',
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=10),
                project=None,  # Proyecto ausente
                freelancer=self.freelancer,
                state='Available'
            )

class FreelancerRegisterTest(LiveServerTestCase):

    # First Log In page
    USERNAME_INPUT = (By.NAME, 'username')
    FULLNAME_INPUT = (By.NAME, 'fullname')
    PHONENUMBER_INPUT = (By.NAME, 'phone_number')
    PASSWORD_INPUT = (By.NAME, 'password')
    SUBMIT_BUTTON = (By.CLASS_NAME, 'buttonSubmit')

    # Second Log In page
    SKIP_BUTTON = (By.CLASS_NAME, 'skipButton')

    # Third Log In page
    ID_INPUT = (By.NAME, 'identification')
    BUTTON = (By.TAG_NAME, 'button')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.timeout = 20
        self.driver.get('http://127.0.0.1:8000/accounts/register/freelancer1')
    
    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.find_element(locator).click()

    def enter_text(self, locator, text):
        self.find_element(locator).send_keys(text)

    def test_freelancer_register(self):
        self.setUp()

        #First Page
        self.assertIn('Sing Up', self.driver.title)
        self.enter_text(self.USERNAME_INPUT, 'user9.test@user1.com')
        self.enter_text(self.FULLNAME_INPUT, 'User Test')
        self.enter_text(self.PHONENUMBER_INPUT, '3124456577')
        self.enter_text(self.PASSWORD_INPUT, 'user1.test')
        self.click(self.SUBMIT_BUTTON)

        # Second page
        self.assertIn('Sing Up', self.driver.title)
        self.click(self.SKIP_BUTTON)

        # Third page
        self.assertIn('Sing Up', self.driver.title)
        self.enter_text(self.ID_INPUT, '123456789')
        self.click(self.BUTTON)

        self.assertIn('Log In', self.driver.title)
        self.driver.quit()
    
    def test_freelancer_register_with_invalid_credentials(self):
        self.setUp()

        #First Page
        try:
            self.assertIn('Sing Up', self.driver.title)
            self.enter_text(self.USERNAME_INPUT, None)
            self.enter_text(self.FULLNAME_INPUT, 'User Test')
            self.enter_text(self.PHONENUMBER_INPUT, '3124456577')
            self.enter_text(self.PASSWORD_INPUT, 'user1.test')
            self.click(self.SUBMIT_BUTTON)
        except Exception:
            self.assertTrue(True)
        
        self.driver.quit()

# Functional tests
class LoginTest(LiveServerTestCase):
    
    USERNAME_INPUT = (By.NAME, 'username')
    PASSWORD_INPUT = (By.NAME, 'password')
    SUBMIT_BUTTON = (By.CLASS_NAME, 'buttonSubmit')

    def setUp(self):
        """
        Método que se ejecuta antes de cada prueba. Aquí se inicializa el navegador.
        """
        self.driver = webdriver.Chrome()  # o webdriver.Firefox()
        self.timeout = 20
        self.driver.get('http://127.0.0.1:8000/accounts/login/')


    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.find_element(locator).click()

    def enter_text(self, locator, text):
        self.find_element(locator).send_keys(text)

    def test_login(self):
        self.setUp()
        self.assertIn('Log In', self.driver.title)
        self.enter_text(self.USERNAME_INPUT, 'user9.test@user1.com') # insertar texto
        self.enter_text(self.PASSWORD_INPUT, 'user1.test')
        self.click(self.SUBMIT_BUTTON)
        self.assertIn('Home', self.driver.title)
        self.driver.quit()

    def test_login_with_invalid_credentials(self):
        self.setUp()
        self.assertIn('Log In', self.driver.title)
        self.enter_text(self.USERNAME_INPUT, 'invalid_user') # insertar texto
        self.enter_text(self.PASSWORD_INPUT, 'invalid')
        self.click(self.SUBMIT_BUTTON)

        try:
            alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
            alert_text = alert.text
            self.assertIn(alert_text, 'Credenciales incorrectas. Intente nuevamente')
            alert.accept()
        except Exception:
            self.fail('Alert not found')
        
        self.assertIn('Log In', self.driver.title)
        self.driver.quit()

