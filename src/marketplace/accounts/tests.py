from django.test import TestCase, Client
from django.urls import reverse
from my_aplication.models import CompanyManager, Project, Milestone

class TestProjectViews(TestCase):

    def setUp(self):
        # Set up test data
        self.client_manager = CompanyManager.objects.create(
            username="manager1",
            email="manager1@example.com",
            password="password123",
            name="Manager One",
        )
        
        self.project = Project.objects.create(
            manager=self.client_manager,
            name="Test Project",
            description="Test Description",
            budget=1000.00,
        )
        
        self.milestone1 = Milestone.objects.create(
            name="Milestone 1",
            description="Milestone description",
            start_date="2024-01-01",
            end_date="2024-01-10",
            project=self.project,
        )

        self.milestone2 = Milestone.objects.create(
            name="Milestone 2",
            description="Milestone description 2",
            start_date="2024-01-11",
            end_date="2024-01-20",
            project=self.project,
        )

        self.client = Client()

    def test_create_project_view(self):
        url = reverse('create_project', args=[self.client_manager.id])
        response = self.client.get(url)

        # Assert response status
        self.assertEqual(response.status_code, 200)

        # Assert template used
        self.assertTemplateUsed(response, 'AddProject.html')

        # Assert context data
        self.assertEqual(response.context['company_manager'], self.client_manager)
        self.assertIn('profile_image', response.context)
        self.assertIn('home_url', response.context)
        self.assertIn('profile_url', response.context)

    def test_edit_project_view(self):
        url = reverse('edit_project', args=[self.client_manager.id, self.project.id])
        response = self.client.get(url)

        # Assert response status
        self.assertEqual(response.status_code, 200)

        # Assert template used
        self.assertTemplateUsed(response, 'EditProject.html')

        # Assert context data
        self.assertEqual(response.context['project'], self.project)
        self.assertQuerysetEqual(
            response.context['milestones'],
            Milestone.objects.filter(project=self.project),
            ordered=False
        )
        self.assertIn('profile_image', response.context)
        self.assertIn('home_url', response.context)
        self.assertIn('profile_url', response.context)