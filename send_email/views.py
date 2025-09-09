import os
from email.mime.image import MIMEImage

from django.conf import settings

# from .token_generator import account_activation_token
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView


# from mailchimp_marketing import Client
# from mailchimp_marketing.api_client import ApiClientError


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

#
# def usersignup(request):
#     if request.method == 'POST':
#         form = UserSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             email_subject = 'Activate Your Account'
#             message = render_to_string('activate_account.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(email_subject, message, to=[to_email])
#             email.send()
#             return HttpResponse(
#                 'We have sent you an email, please confirm your email address to complete registration')
#     else:
#         form = UserSignUpForm()
#     return render(request, 'signup.html', {'form': form})
#
#
# def activate_account(request, uidb64, token):
#     try:
#         uid = force_bytes(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return HttpResponse('Your account has been activate successfully')
#     else:
#         return HttpResponse('Activation link is invalid!')
#
#
# api_key = settings.MAILCHIMP_API_KEY
# server = settings.MAILCHIMP_DATA_CENTER
# list_id = settings.MAILCHIMP_EMAIL_LIST_ID
#
#
# # Subscription Logic
# def subscribe(email):
#     """
#      Contains code handling the communication to the mailchimp api
#      to create a contact/member in an audience/list.
#     """
#
#     mailchimp = Client()
#     mailchimp.set_config({
#         "api_key": api_key,
#         "server": server,
#     })
#
#     member_info = {
#         "email_address": email,
#         "status": "subscribed",
#     }
#
#     try:
#         response = mailchimp.lists.add_list_member(list_id, member_info)
#         print("response: {}".format(response))
#     except ApiClientError as error:
#         print("An exception occurred: {}".format(error.text))
#
#
# def subscription(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         print(email)
#         subscribe(email)
#         messages.success(request, "Email received. thank You! ")
#
#     return render(request, "subscription.html")
