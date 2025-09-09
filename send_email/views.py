import os
from email.mime.image import MIMEImage

from django.conf import settings

from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView


class SimpleEmailTemplateView(TemplateView):
    template_name = "hello_email.html"

    def get(self, request, *args, **kwargs):
        html_content = render_to_string(self.template_name, context={})

        send_mail(
            "Лист з хтмл",
            "Мій пробний html-лист",
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            html_message=html_content,
            fail_silently=True,
        )
        return render(request, self.template_name)


class ImageEmailTemplateView(TemplateView):
    template_name = "hello_email.html"

    def logo_data(self, image_name):
        print(image_name)
        with open(os.path.join(os.path.join(settings.MEDIA_ROOT), image_name), "rb") as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header("Content-ID", f"<{image_name}>")
        logo.add_header("Content-Disposition", "inline", filename=image_name)
        return logo

    def get(self, request, *args, **kwargs):
        html_content = render_to_string(self.template_name, context={"my_name": "EugeneZ lab"})

        email_message = EmailMultiAlternatives(
            subject="Якийсь Subject",
            body="якийсь тестовий зміст",
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.mixed_subtype = "related"
        for image in os.listdir(os.path.join(settings.MEDIA_ROOT)):
            email_message.attach(self.logo_data(image))
        email_message.send(fail_silently=False)

        return render(request, self.template_name)
