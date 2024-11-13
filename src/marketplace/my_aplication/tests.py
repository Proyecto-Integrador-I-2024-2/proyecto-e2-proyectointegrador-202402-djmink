from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from .models import Freelancer, CompanyManager, Project, Rating, Skill, Application, Milestone
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError



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

class RatingModelTest(TestCase):
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
        
        # Obtener el ContentType correcto para Freelancer
        freelancer_type = ContentType.objects.get_for_model(Freelancer)
        
        # Crear una instancia de Rating usando el ContentType correcto
        self.rating = Rating.objects.create(
            content_type=freelancer_type,
            object_id=self.freelancer.id,
            user=self.freelancer,
            score=4.5
        )

    def test_create_rating(self):
        # Verifica que la calificación se haya creado correctamente
        self.assertEqual(self.rating.content_type.model, 'freelancer')
        self.assertEqual(self.rating.object_id, self.freelancer.id)
        self.assertEqual(self.rating.user, self.freelancer)
        self.assertEqual(self.rating.score, 4.5)

    def test_rating_score_value(self):
        # Verifica que el puntaje esté dentro del rango permitido
        self.assertTrue(1 <= self.rating.score <= 5, "Score debe estar entre 1 y 5.")

    def test_content_type_association(self):
        # Verifica que el content_type sea el correcto
        freelancer_type = ContentType.objects.get_for_model(Freelancer)
        self.assertEqual(self.rating.content_type, freelancer_type)

    def test_rating_retrieval(self):
        # Verifica que se pueda recuperar la calificación usando object_id y content_type
        retrieved_rating = Rating.objects.get(content_type=self.rating.content_type, object_id=self.freelancer.id)
        self.assertEqual(retrieved_rating, self.rating)
    


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
    
##Pruebas negativas unitarias
