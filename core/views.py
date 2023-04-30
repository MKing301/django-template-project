import os
import pandas as pd
import openpyxl
import json
import datetime

from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, logout_then_login
from django.contrib.auth import (
    login, logout, authenticate, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, City, Usr_State, Profile
from .forms import (
    AuthenticationFormWithCaptchaField,
    NewUserForm,
    UserUpdateForm,
    ProfileUpdateForm,
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


def check_username(request):
    username = request.POST.get('username')
    try:
        user = User.objects.get(username=username)
        return HttpResponse('<div id="username-error" class="error">This username already exists!</div>')
    except User.DoesNotExist:
        return HttpResponse('<div id="username-error" class="success">This username is available.</div>')


def check_email(request):
    email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
        return HttpResponse('<div id="email-error" class="error">This email already exists!</div>')
    except User.DoesNotExist:
        return HttpResponse('<div id="email-error" class="success">This email is available.</div>')


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

                # START AUTOMATICALLY ALLOW USERS TO ACCESS APP
                ''' user = authenticate(username=username, password=password)
                login(request, user)
                form.send_registration_email()
                messages.success(
                    request,
                    f"New account created for {username}."
                )
                messages.success(
                    request,
                    f"Successfully logged in as {username}."
                ) '''
                # END AUTOMATICALLY ALLOW USERS TO ACCESS APP

                # START USER ACTIVE SET TO FALSE BY DEFAULT
                form.send_registration_email()
                messages.info(
                    request,
                    f"Email sent to Admin to activate your account."
                )
                # END USER ACTIVE SET TO FALSE BY DEFAULT
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
def profile(request):

    usr = User.objects.get(id=request.user.id)
    prfle = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=usr)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=prfle)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('core:profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=usr)
        p_form = ProfileUpdateForm(instance=prfle)

    city_list = City.objects.all()
    state_list = Usr_State.objects.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'usr': usr,
        'prfle': prfle,
        'city_list': city_list,
        'state_list': state_list
    }

    return render(
        request,
        'core/profile.html',
        context
    )


@login_required
def members(request):

    gender_labels = []
    gender_data = []
    marital_labels = []
    marital_data = []
    city_labels = []
    city_data = []
    tier_labels = []
    tier_data = []

    QUERY = """
    SELECT
	au.id,
	au.first_name,
	au.last_name,
	au.email,
	cp.gender,
	cp.marital_status,
	cp.tier,
	cp.street_number,
	cp.street_name,
	cc.name,
	cus.name,
	cp.postal_code
    FROM auth_user au, core_profile cp, core_city cc, core_usr_state cus
    WHERE au.id = cp.user_id
    and cp.usr_city_id = cc.id
    and cus.id = cc.selected_state_id
    ORDER BY au.last_name, au.first_name
    """

    data_list = []
    with connection.cursor() as cur:
        row = cur.execute(QUERY,)
        for row in cur:
            data_list.append({
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'gender': row[4],
                'marital_status': row[5],
                'tier': row[6],
                'street_number': row[7],
                'street_name': row[8],
                'city': row[9],
                'state_abbrev': row[10],
                'postal_code': row[11],
            })

    gender_df = pd.DataFrame(list(data_list))
    gender_group = gender_df.groupby(['gender'])['first_name'].count().reset_index(name='count')

    for index, row in gender_group.iterrows():
        gender_labels.append(row['gender'])
        gender_data.append(row['count'])

    marital_df = pd.DataFrame(list(data_list))
    marital_group = marital_df.groupby(['marital_status'])['first_name'].count().reset_index(name='count')

    for index, row in marital_group.iterrows():
        marital_labels.append(row['marital_status'])
        marital_data.append(row['count'])

    city_df = pd.DataFrame(list(data_list))
    city_group = city_df.groupby(['city'])['first_name'].count().reset_index(name='count')

    for index, row in city_group.iterrows():
        city_labels.append(row['city'])
        city_data.append(row['count'])

    tier_df = pd.DataFrame(list(data_list))
    tier_group = tier_df.groupby(['tier'])['first_name'].count().reset_index(name='count')

    for index, row in tier_group.iterrows():
        tier_labels.append(row['tier'])
        tier_data.append(row['count'])

    return render(
        request=request,
        template_name="core/members.html",
        context={
            'data_list': data_list,
            'gender_labels': gender_labels,
            'gender_data': gender_data,
            'marital_labels': marital_labels,
            'marital_data': marital_data,
            'city_labels': city_labels,
            'city_data': city_data,
            'tier_labels': tier_labels,
            'tier_data': tier_data
        }
    )


@login_required
def finances(request):
    num_tithe_donors = []
    tithe_amount = []
    num_church_budget_donors = []
    church_budget_amount = []
    month_year = []
    total_local_funds_amount = []

    wb = openpyxl.load_workbook('/home/mfsd1809/dev-environment/FullStackWebDeveloper/Gethsemane/report.xlsx')
    for sheet in wb.worksheets:
        month_year.append(sheet.title.replace(',', ''))
        for row in range(1, sheet.max_row + 1):
            if sheet['A' + str(row)].value == 'Tithe':
                num_tithe_donors.append(sheet['B' + str(row)].value)
                tithe_amount.append(sheet['D' + str(row)].value)
            if sheet['A' + str(row)].value == 'Church Budget':
                num_church_budget_donors.append(sheet['B' + str(row)].value)
                church_budget_amount.append(sheet['D' + str(row)].value)
            if sheet['A' + str(row)].value == 'Local Funds':
                total_local_funds_amount.append(sheet['D' + str(row)].value)
            else:
                pass

    # Reverse lists for oldest to newest values
    num_tithe_donors.reverse()
    tithe_amount.reverse()
    num_church_budget_donors.reverse()
    church_budget_amount.reverse()
    month_year.reverse()
    total_local_funds_amount.reverse()



    # Create a zipped list of tuples from above lists
    zippedList =  list(zip(month_year, num_tithe_donors, tithe_amount, num_church_budget_donors, church_budget_amount, total_local_funds_amount))

    # Create a dataframe from zipped list
    df = pd.DataFrame(zippedList, columns = [
        'month_year' ,
        'number_tithe_donors',
        'tithe',
        'number_church_budget_donors',
        'church_budget',
        'total_local_funds'])

    # Set index to start at 1; 0 is the default
    df.index = df.index + 1

    labels = df['month_year'].values.tolist()
    values = df['church_budget'].values.tolist()

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    return render(
        request=request,
        template_name="core/finances.html",
        context={
            'data': data,
            'labels': labels,
            'values': values
        }
    )


@login_required
def logout_request(request):
    return logout_then_login(request, login_url='/')
