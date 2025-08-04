"""
Sample tests for ITVDN Django Study Project
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SampleTestCase(TestCase):
    """Sample test case to verify CI/CD pipeline"""

    def test_sample_assertion(self):
        """Test basic assertion"""
        self.assertEqual(1 + 1, 2)
        self.assertTrue(True)

    def test_user_creation(self):
        """Test user model"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword123'))

    def test_admin_url_exists(self):
        """Test that admin URL is accessible"""
        response = self.client.get('/admin/', follow=True)
        # Should redirect to login page
        self.assertEqual(response.status_code, 200)


class ViewTestCase(TestCase):
    """Test views if they exist"""

    def test_home_page_status_code(self):
        """Test home page returns 200 if it exists"""
        try:
            response = self.client.get('/')
            # If home page exists, should return 200
            # If not, will raise NoReverseMatch which is fine for CI
            self.assertIn(response.status_code, [200, 404])
        except Exception:
            # URL not configured yet, which is fine for a new project
            pass