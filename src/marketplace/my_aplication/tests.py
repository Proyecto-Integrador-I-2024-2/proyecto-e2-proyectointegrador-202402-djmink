from django.test import TestCase
from django.urls import reverse

<<<<<<< HEAD
# Create your tests here.

   
    
=======
class HomeViewTest(TestCase):
    
    """Tests for the Home view."""

    def test_home_view_status_code(self):
        """
        Test that the home page returns a 200 status code.
        
        This test checks if the home view is accessible and returns a
        successful HTTP 200 response when the page is loaded.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        """
        Test that the correct template is used for the home view.
        
        This test verifies if the correct template `home.html` is rendered 
        when the user visits the home page.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'my_aplication/first_page.html')
>>>>>>> dev
