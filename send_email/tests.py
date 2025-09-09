import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from django.test import TestCase, RequestFactory, override_settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage

from send_email.views import SimpleEmailTemplateView, ImageEmailTemplateView


class SimpleEmailTemplateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = SimpleEmailTemplateView()

    @patch('send_email.views.send_mail')
    @patch('send_email.views.render_to_string')
    @patch('send_email.views.render')
    def test_get_sends_simple_email(self, mock_render, mock_render_to_string, mock_send_mail):
        """Test that GET request sends a simple email with correct parameters"""
        # Setup
        mock_render_to_string.return_value = "<html>Test content</html>"
        mock_render.return_value = "rendered_response"
        request = self.factory.get('/test/')

        # Execute
        response = self.view.get(request)

        # Assert
        mock_render_to_string.assert_called_once_with("hello_email.html", context={})
        mock_send_mail.assert_called_once_with(
            "Лист з хтмл",
            "Мій пробний html-лист",
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            html_message="<html>Test content</html>",
            fail_silently=True,
        )
        mock_render.assert_called_once_with(request, "hello_email.html")
        self.assertEqual(response, "rendered_response")

    @patch('send_email.views.render')
    @patch('send_email.views.send_mail')
    @patch('send_email.views.render_to_string')
    def test_get_handles_send_mail_failure_silently(self, mock_render_to_string, mock_send_mail, mock_render):
        """Test that send_mail is called with fail_silently=True parameter"""
        # Setup
        mock_render_to_string.return_value = "<html>Test</html>"
        mock_render.return_value = "rendered_response"
        # Don't make send_mail raise exception - just verify it's called correctly
        mock_send_mail.return_value = True
        request = self.factory.get('/test/')

        # Execute
        response = self.view.get(request)

        # Assert that send_mail was called with fail_silently=True
        mock_send_mail.assert_called_once_with(
            "Лист з хтмл",
            "Мій пробний html-лист",
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            html_message="<html>Test</html>",
            fail_silently=True,
        )
        # Should render the template successfully
        self.assertEqual(response, "rendered_response")


class ImageEmailTemplateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = ImageEmailTemplateView()
        self.test_media_root = tempfile.mkdtemp()

    @override_settings(MEDIA_ROOT='/test/media/')
    def test_logo_data_reads_image_file(self):
        """Test that logo_data correctly reads and creates MIMEImage"""
        # Setup
        test_image_data = b'fake_image_data'
        image_name = 'test_logo.png'

        with patch('builtins.open', mock_open(read_data=test_image_data)):
            with patch('send_email.views.MIMEImage') as mock_mime_image:
                mock_logo = MagicMock()
                mock_mime_image.return_value = mock_logo

                # Execute
                result = self.view.logo_data(image_name)

                # Assert
                mock_mime_image.assert_called_once_with(test_image_data)
                mock_logo.add_header.assert_any_call("Content-ID", f"<{image_name}>")
                mock_logo.add_header.assert_any_call("Content-Disposition", "inline", filename=image_name)
                self.assertEqual(result, mock_logo)

    @override_settings(MEDIA_ROOT='/test/media/')
    def test_logo_data_file_path_construction(self):
        """Test that logo_data constructs correct file path"""
        image_name = 'test.jpg'
        expected_path = '/test/media/test.jpg'

        with patch('builtins.open', mock_open(read_data=b'data')) as mock_file:
            with patch('send_email.views.MIMEImage'):
                # Execute
                self.view.logo_data(image_name)

                # Assert
                mock_file.assert_called_once_with(expected_path, "rb")

    @patch('send_email.views.os.listdir')
    @patch('send_email.views.render_to_string')
    @patch('send_email.views.render')
    def test_get_sends_email_with_attachments(self, mock_render, mock_render_to_string, mock_listdir):
        """Test that GET request sends email with image attachments"""
        # Setup
        mock_render_to_string.return_value = "<html>Test with {{my_name}}</html>"
        mock_render.return_value = "rendered_response"
        mock_listdir.return_value = ['image1.jpg', 'image2.png']
        request = self.factory.get('/test/')

        with patch.object(self.view, 'logo_data') as mock_logo_data:
            mock_logo1 = MagicMock()
            mock_logo2 = MagicMock()
            mock_logo_data.side_effect = [mock_logo1, mock_logo2]

            with patch('send_email.views.EmailMultiAlternatives') as mock_email_class:
                mock_email = MagicMock()
                mock_email_class.return_value = mock_email

                # Execute
                response = self.view.get(request)

                # Assert template rendering
                mock_render_to_string.assert_called_once_with(
                    "hello_email.html",
                    context={"my_name": "EugeneZ lab"}
                )

                # Assert email creation
                mock_email_class.assert_called_once_with(
                    subject="Якийсь Subject",
                    body="якийсь тестовий зміст",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[settings.EMAIL_HOST_USER],
                )

                # Assert email configuration
                mock_email.attach_alternative.assert_called_once_with(
                    "<html>Test with {{my_name}}</html>",
                    "text/html"
                )
                self.assertEqual(mock_email.mixed_subtype, "related")

                # Assert attachments
                mock_logo_data.assert_any_call('image1.jpg')
                mock_logo_data.assert_any_call('image2.png')
                self.assertEqual(mock_logo_data.call_count, 2)

                mock_email.attach.assert_any_call(mock_logo1)
                mock_email.attach.assert_any_call(mock_logo2)
                self.assertEqual(mock_email.attach.call_count, 2)

                # Assert email sending
                mock_email.send.assert_called_once_with(fail_silently=False)

    @patch('send_email.views.os.listdir')
    @patch('send_email.views.render_to_string')
    def test_get_handles_empty_media_directory(self, mock_render_to_string, mock_listdir):
        """Test behavior when media directory is empty"""
        # Setup
        mock_render_to_string.return_value = "<html>Test</html>"
        mock_listdir.return_value = []  # Empty directory
        request = self.factory.get('/test/')

        with patch('send_email.views.EmailMultiAlternatives') as mock_email_class:
            mock_email = MagicMock()
            mock_email_class.return_value = mock_email

            # Execute
            response = self.view.get(request)

            # Assert
            mock_email.attach.assert_not_called()  # No attachments
            mock_email.send.assert_called_once()

    @patch('send_email.views.os.listdir')
    @patch('send_email.views.render_to_string')
    def test_get_handles_email_send_failure(self, mock_render_to_string, mock_listdir):
        """Test that email send failures are not silently ignored"""
        # Setup
        mock_render_to_string.return_value = "<html>Test</html>"
        mock_listdir.return_value = ['test.jpg']
        request = self.factory.get('/test/')

        with patch.object(self.view, 'logo_data') as mock_logo_data:
            mock_logo_data.return_value = MagicMock()

            with patch('send_email.views.EmailMultiAlternatives') as mock_email_class:
                mock_email = MagicMock()
                mock_email.send.side_effect = Exception("SMTP Error")
                mock_email_class.return_value = mock_email

                # Execute & Assert
                with self.assertRaises(Exception):
                    self.view.get(request)

    @override_settings(MEDIA_ROOT='/nonexistent/')
    def test_logo_data_handles_file_not_found(self):
        """Test logo_data behavior when image file doesn't exist"""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            with self.assertRaises(FileNotFoundError):
                self.view.logo_data('nonexistent.jpg')

    @patch('send_email.views.os.listdir')
    def test_get_handles_media_directory_not_found(self, mock_listdir):
        """Test behavior when media directory doesn't exist"""
        mock_listdir.side_effect = FileNotFoundError("Directory not found")
        request = self.factory.get('/test/')

        with self.assertRaises(FileNotFoundError):
            self.view.get(request)


class EmailViewsIntegrationTest(TestCase):
    """Integration tests that test the views with minimal mocking"""

    def setUp(self):
        self.factory = RequestFactory()

    @patch('send_email.views.send_mail')
    @patch('send_email.views.render')
    def test_simple_email_view_template_rendering(self, mock_render, mock_send_mail):
        """Test that SimpleEmailTemplateView properly renders templates"""
        view = SimpleEmailTemplateView()
        request = self.factory.get('/test/')
        mock_render.return_value = "rendered_response"

        # Execute
        response = view.get(request)

        # Assert that render was called with correct template
        mock_render.assert_called_once_with(request, "hello_email.html")
        self.assertEqual(response, "rendered_response")

    def test_view_attributes(self):
        """Test that views have correct template names"""
        simple_view = SimpleEmailTemplateView()
        image_view = ImageEmailTemplateView()

        self.assertEqual(simple_view.template_name, "hello_email.html")
        self.assertEqual(image_view.template_name, "hello_email.html")


# Additional edge case tests
class EmailViewsEdgeCaseTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.image_view = ImageEmailTemplateView()

    @patch('send_email.views.os.listdir')
    def test_image_view_handles_permission_error(self, mock_listdir):
        """Test handling of permission errors when accessing media directory"""
        mock_listdir.side_effect = PermissionError("Permission denied")
        request = self.factory.get('/test/')

        with self.assertRaises(PermissionError):
            self.image_view.get(request)

    def test_logo_data_prints_image_name(self):
        """Test that logo_data prints the image name (as per original code)"""
        with patch('builtins.print') as mock_print:
            with patch('builtins.open', mock_open(read_data=b'data')):
                with patch('send_email.views.MIMEImage'):
                    self.image_view.logo_data('test.jpg')
                    mock_print.assert_called_once_with('test.jpg')
