from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout, login
from django.shortcuts import redirect, get_object_or_404
from .forms import UserRegistrationForm, EditProfileForm, EntryDepartmentForm, InputBulkUserForm
from .models import Profile, Department
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.views import View
from django.contrib.auth.models import User
import pandas as pd
from django.contrib.auth.hashers import make_password


@login_required(login_url='login')
def home(request):
    return render(request, 'users/home.html')


class InputBulkUsersView(View):
    def get(self, request):
        form = InputBulkUserForm()
        context = {
            'form': form,
        }
        return render(request, 'users/input_bulk_user.html', context)

    def post(self, request):
        form = InputBulkUserForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            df = pd.read_csv(cd['file_content'])
            for index, row in df.iterrows():
                username = row['username']
                first_name = row['first_name']
                last_name = row['last_name']
                email = row['email']
                password = make_password("Asmin2022")
                User.objects.update_or_create(username=username, first_name=first_name, last_name=last_name,
                                              email=email,
                                              password=password)
            messages.success(request, "Input Bulk Users has been processed")
            return redirect('home')
        else:
            print(form.errors)
            print(form.fields)
            messages.error(request, "Data is not valid!")
            form = InputBulkUserForm()
            context = {
                'form': form,
            }
            return render(request, 'users/input_bulk_user.html', context)


def register(request):
    username = ""
    first_name = ""
    last_name = ""
    email = ""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User Account was created.')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    }
    return render(request, 'users/signup.html', context)


class EditProfileView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        prof = user.user2profile

        form = EditProfileForm(instance=prof)

        context = {
            'form': form,
        }
        return render(request, 'users/edit_profile.html', context)

    def post(self, request):
        curr_prof = Profile.objects.get(profile2user=request.user)
        form = EditProfileForm(request.POST, request.FILES, instance=curr_prof)

        if form.is_valid():
            form.save()
            messages.success(request, "Update profile successfully!")
            return redirect('home')
        else:
            print(form)
            print(form.errors)
            context = {
                'form': form,
            }
            return render(request, 'users/edit_profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    departments = Department.objects.all()
    prof = user.user2profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Update User model
            cd = form.cleaned_data
            # print(cd)
            usr = request.user
            usr.email = cd['email']
            usr.first_name = cd['first_name']
            usr.last_name = cd['last_name']
            usr.save()
            # Update Profile model
            prof = usr.user2profile
            prof.gender = cd['gender']
            prof.location = cd['location']
            prof.mobile = cd['mobile']
            prof.bod = cd['bod']
            if cd['photo'] is not None:
                prof.photo = cd['photo']
            obj_profdept = get_object_or_404(Department, pk=cd['profile2department'])
            prof.profile2department = obj_profdept
            prof.save()
            messages.success(request, "Profile berhasil di update.")
            return redirect('home')
        else:
            if request.POST.get('first_name') == '':
                messages.error(request, "First Name must be filled!")
            if request.POST.get('last_name') == '':
                messages.error(request, "Last Name must be filled!")
            print(form)
            print("Invalid form")
            print(form.errors)
    form = EditProfileForm()
    context = {
        'form': form,
        'departments': departments,
        'prof': prof,
        'user': user,
    }
    return render(request, 'users/edit_profile.html', context)


# def input_department(request):
#     current_dept = Department.objects.all()
#     if request.method == "POST":
#         form = EntryDepartmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Data Department has been saved!")
#             return redirect('users:input_department')
#     else:
#         form = EntryDepartmentForm()
#     context = {
#         'form': form,
#         'current_dept': current_dept,
#     }
#     return render(request, 'users/input_department.html', context)

class EntryDepartmentView(View):
    def get(self, request):
        form = EntryDepartmentForm()
        departments = Department.objects.all()
        context = {
            'form': form,
            'departments': departments,
        }
        return render(request, 'users/input_department.html', context)

    def post(self, request):
        form = EntryDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Department has been saved!")
        else:
            departments = Department.objects.all()
            context = {
                'form': form,
                'departments': departments,
            }
            return render(request, 'users/input_department.html', context)
        form = EntryDepartmentForm()
        departments = Department.objects.all()
        context = {
            'form': form,
            'departments': departments,
        }
        return render(request, 'users/input_department.html', context)
