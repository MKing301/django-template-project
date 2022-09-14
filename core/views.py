import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, logout_then_login
from django.contrib.auth import (
    login, logout, authenticate, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    AuthenticationFormWithCaptchaField,
    NewUserForm,
    EditProfileForm,
    ContactForm
)
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy
from .signals import log_user_logout


class PasswordsChangeView(PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    success_url = reverse_lazy('core:password_changed')


@login_required
def password_changed(request):
    return render(
        request=request,
        template_name='accounts/password_changed.html'
    )


@login_required
def password_change_request(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request,
                "Your password was updated successfully."
            )
            return redirect('core:profile')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(
            request=request,
            template_name="accounts/password_change.html",
            context=args
        )


def password_reset_complete(request):
    return render(
        request=request,
        template_name='accounts/password_reset_complete.html'
    )


def index(request):
    return render(request=request,
                  template_name="core/index.html"
                  )


def entry(request):
    return render(request=request,
                  template_name="core/entry.html"
                  )



def login_request(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationFormWithCaptchaField(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(
                    request,
                    f'{username} logged in successfully.'
                )
                return redirect("core:entry")

            elif User.objects.filter(
                    username=form.cleaned_data.get('username')).exists():
                user = User.objects.filter(
                    username=form.cleaned_data.get('username')).values()
                if(user[0]['is_active'] is False):
                    messages.info(
                        request,
                        "Contact the administrator to activate your account!"
                    )
                    return redirect("core:login_request")

                else:
                    return render(
                        request=request,
                        template_name="registration/login.html",
                        context={"form": form}
                    )

            else:
                return render(
                    request=request,
                    template_name="registration/login.html",
                    context={"form": form}
                )
        else:
            form = AuthenticationFormWithCaptchaField()
            return render(
                request=request,
                template_name="registration/login.html",
                context={"form": form}
            )
    else:
        messages.info(
            request,
            '''You are already logged in.  You must log out to log in as
            another user.'''
        )
        return redirect("core:index")


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                form.save()
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(
                    request,
                    f"New account created for {username}."
                )
                messages.success(
                    request,
                    f"Successfully logged in as {username}."
                )

                subject, from_email, to = 'New User Registered for core App', os.environ.get(
                    'MAIL_USERNAME'), os.environ.get('MAIL_RECIPIENTS')
                text_content = f'''
                New User ...

                First Name: {first_name}\n
                Last Name: {last_name}\n
                Username: {username}\n
                Email: {email}\n
                '''
                html_content = f'''
                <p>Greetings!</p>
                <p>The following user registered:</p>
                <ul>
                <li><strong>First Name:</strong> {first_name}</li>
                <li><strong>Last Name:</strong> {last_name}</li>
                <li><strong>Username:</strong> {username}</li>
                <li><strong>Email:</strong> {email}</li>
                </ul>
                '''
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect("core:entry")
            else:
                return render(
                    request=request,
                    template_name="registration/register.html",
                    context={"form": form}
                )
        else:

            form = NewUserForm
            return render(
                request=request,
                template_name="registration/register.html",
                context={"form": form}
            )
    else:
        messages.info(
            request,
            '''You are already registered.  You must log out to register
            another user.'''
        )
        return redirect("core:index")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            contact_email = form.cleaned_data.get("contact_email")
            contact_subject = form.cleaned_data.get("contact_subject")
            contact_message = form.cleaned_data.get("contact_message")

            subject, from_email, to = contact_subject, os.environ.get(
                'MAIL_USERNAME'), os.environ.get('MAIL_RECIPIENTS')
            text_content = f'''
            Message from ...

            Full Name: {fullname}\n
            Email Address: {contact_email}\n
            Contact Message: {contact_message}
            '''
            html_content = f'''
                <p>Message from core App User...</p>

                <p><strong>Full Name:</strong> {fullname}</p>
                <p><strong>Email Address:</strong> {contact_email}</p>
                <p><strong>Message:</strong> {contact_message}</p>
                '''
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(
                request,
                "Email sent!  Thank you for contacting us."
            )
            return redirect("core:index")
        else:
            return render(
                request=request,
                template_name="core/contact.html",
                context={"form": form}
            )

    form = ContactForm
    return render(
        request=request,
        template_name="core/contact.html",
        context={"form": form}
    )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile was updated successfully."
            )
            return redirect('core:view_profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(
            request=request,
            template_name="core/edit_profile.html",
            context=args
        )


@login_required
def logout_request(request):
    return logout_then_login(request, login_url='/')
