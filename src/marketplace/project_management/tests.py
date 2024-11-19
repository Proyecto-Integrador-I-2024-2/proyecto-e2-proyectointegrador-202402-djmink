from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from my_aplication.models import Project, User, Freelancer, CompanyManager, Like, ProjectComment, Milestone, Application, Rating
from django.contrib.contenttypes.models import ContentType

class FreelancerProjectViewTest(TestCase):
    def setUp(self):
    # Create a CompanyManager
        self.company_manager = CompanyManager.objects.create(
            username="company_manager",
            email="manager@example.com",
            password="password123",
            name="Manager",
        )
        
        # Create a Freelancer
        self.freelancer = Freelancer.objects.create(
            username="freelancer",
            email="freelancer@example.com",
            password="password123",
            name="Freelancer",
            profession="Developer",
            price="50/hr",
        )
        
        # Create a Project
        self.project = Project.objects.create(
            manager=self.company_manager,
            name="Test Project",
            description="A test project",
            budget=5000.00,
            state="PENDING",
        )
        
        # Create Milestones
        self.milestone = Milestone.objects.create(
            name="Milestone 1",
            description="Complete phase 1",
            start_date=now().date(),
            end_date=now().date(),
            project=self.project,
        )

        # Create Comments
        self.comment = ProjectComment.objects.create(
            author="Freelancer",
            content="This looks great!",
            project=self.project,
            user=self.freelancer,
        )

        # Create Likes
        self.like = Like.objects.create(
            project=self.project,
            content_type=ContentType.objects.get_for_model(Project),
            object_id=self.freelancer.id,
            user=self.freelancer,
        )
        
        # Create Applications
        self.application = Application.objects.create(
            freelancer=self.freelancer,
            project=self.project,
            milestone=self.milestone,
            state="Sent",
        )

        self.client = Client()

    def test_freelancer_view(self):
        """Test the view when accessed by a Freelancer."""
        url = reverse('freelancer_project', args=[self.freelancer.id, self.project.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Verify context data
        self.assertIn('p', response.context)
        self.assertEqual(response.context['p'], self.project)
        self.assertIn('m', response.context)
        self.assertIn(self.milestone, response.context['m'])
        self.assertIn('c', response.context)
        self.assertIn(self.comment, response.context['c'])
        self.assertIn('rating', response.context)
        self.assertIn('likes', response.context)
        self.assertEqual(response.context['likes'], 1)  # One like

        # Verify freelancer-specific context
        self.assertIn('freelancer', response.context)
        self.assertEqual(response.context['freelancer'], self.freelancer)
        self.assertTrue(response.context['freelancer'].has_applied)

    def test_company_manager_view(self):
        """Test the view when accessed by a CompanyManager."""
        url = reverse('freelancer_project', args=[self.company_manager.id, self.project.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Verify context data
        self.assertIn('p', response.context)
        self.assertEqual(response.context['p'], self.project)
        self.assertIn('m', response.context)
        self.assertIn(self.milestone, response.context['m'])
        self.assertIn('c', response.context)
        self.assertIn(self.comment, response.context['c'])
        self.assertIn('rating', response.context)
        self.assertIn('likes', response.context)

        # Verify company-manager-specific context
        self.assertIn('freelancer', response.context)
        self.assertEqual(response.context['freelancer'], self.company_manager)

    def test_invalid_project(self):
        """Test when an invalid project ID is given."""
        url = reverse('freelancer_project', args=[self.freelancer.id, 999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_viewer(self):
        """Test when an invalid freelancer/company manager ID is given."""
        url = reverse('freelancer_project', args=[999, self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)