from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Department
from django.shortcuts import get_object_or_404
from .validators import empty_value
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class InputBulkUserForm(forms.Form):
    file_content = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(_("Yor password did not match!"), code="password_unmatch")
        return cd['password2']

    # def clean_email(self):
    #     email_check = self.cleaned_data.get('email')
    #     if email_check:
    #         if 'asmincoal.co.id' in email_check:
    #             pass
    #         else:
    #             if 'turanggaresources.com' in email_check:
    #                 pass
    #             else:
    #                 raise forms.ValidationError(_("Official email must be used. Not general email."),
    #                                             code="invalid_email")
    #     else:
    #         raise forms.ValidationError(_("Email must be filled."), code="email_empty")
    #     return email_check


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ("profile2user", "username", "profile2department", "bod")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_gender(self):
        gender_passed = self.cleaned_data.get('gender', None)
        if gender_passed is None:
            raise forms.ValidationError(_("Gender must be filled!"), code="gender_empty")
        return gender_passed

    # def clean_email(self):
    #     email_check = self.cleaned_data.get('email')
    #     if email_check:
    #         if 'asmincoal.co.id' in email_check:
    #             pass
    #         else:
    #             if 'turanggaresources.com' in email_check:
    #                 pass
    #             else:
    #                 raise forms.ValidationError(_("Official email must be used. Not general email."),
    #                                             code="general_email")
    #     else:
    #         raise forms.ValidationError(_("Email must be filled."), code="empty_email")
    #     return email_check

    # def clean(self):
    #     cleaned_data = super(EditProfileForm, self).clean()
    #     fs_name = cleaned_data.get('first_name')
    #     ls_name = cleaned_data.get('last_name')
    #     if fs_name is None and ls_name is None:
    #         raise forms.ValidationError("First Name and Last Name cannot be emptied!")


class EntryDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name_input = self.cleaned_data.get('name', None)
        if name_input:
            name_data_exist = Department.objects.filter(name__icontains=name_input)
            if name_data_exist:
                raise forms.ValidationError("Departement already taken!")
        else:
            raise forms.ValidationError("Name must be filled!")
        return name_input

    def clean_description(self):
        description_input = self.cleaned_data.get('description', None)
        if description_input is None:
            raise forms.ValidationError("Description must be filled!")
        return description_input

    # def clean(self):
    #     cleaned_data = super(EntryDepartmentForm, self).clean()
    #     name_input = self.cleaned_data.get('name', None)
    #     description_input = self.cleaned_data.get('description', None)
    #
    #     if name_input and description_input:
    #         pass
    #     else:
    #         raise forms.ValidationError("Both fields (name and description) must be filled!")
