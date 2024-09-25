from django.test import TestCase
from django.urls import reverse
from perfil.models import Profile, ClientProfile

class ProfileFreelancerViewTest(TestCase):

    def setUp(self):
        
        self.freelancer_profile = Profile.objects.create(
            name='Freelancer Test',
            email='freelancer@test.com',
            phone='987654321',
            profession='Developer',
            description='Freelancer desc.',
            rating=4.5,
            jobs_completed=5,
            price='$40/hora'
        )

    def test_freelancer_profile_view_status_code(self):
        """
        Test that the freelancer profile view returns a 200 status code.
        """
        url = reverse('perfilFreelancer', kwargs={'id': self.freelancer_profile.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_freelancer_profile_view_template_used(self):
        """
        Test that the correct template is used for the freelancer profile view.
        
        This test verifies if the correct template `perfil_freelancer.html` is rendered 
        when the user visits this page.
        """
        url = reverse('perfilFreelancer', kwargs={'id': self.freelancer_profile.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'perfil/perfil_freelancer.html')

class ProfileClientViewTest(TestCase):

    def setUp(self):
        
        self.client_profile = ClientProfile.objects.create(
            name='Client Test',
            email='client@test.com',
            phone='987654321',
            type='Education',
            description='Client desc.',
            rating=4.5,
        )

    """Tests for the client profile view."""

    def test_client_profile_view_status_code(self):
        """
        Test that the client profile page returns a 200 status code.
        
        This test checks if the client profile view is accessible and returns a
        successful HTTP 200 response when the page is loaded.
        """
        url = reverse('perfilesCliente', kwargs={'id': self.client_profile.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_client_profile_view_template_used(self):
        """
        Test that the correct template is used for the client profile view.
        
        This test verifies if the correct template `perfil_cliente.html` is rendered 
        when the user visits this page.
        """
        url = reverse('perfilesCliente', kwargs={'id': self.client_profile.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'perfil/perfil_cliente.html')

