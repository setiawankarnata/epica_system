from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Meeting, Topic, TopicFile, ActivityFile, Activity, Outside
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget


class NewMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = "__all__"
        exclude = ('meeting2company', 'meeting2user')
        widgets = {
            'meeting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
            'notulen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of notulen'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }


class EntryTopicsForm(forms.ModelForm):
    problem_info = forms.CharField(widget=CKEditorWidget(config_name='default'))
    action = forms.CharField(widget=CKEditorWidget(config_name='default'))

    class Meta:
        model = Topic
        fields = "__all__"
        exclude = ('topic2meeting', 'topic2user', 'new_due_date', 'status', 'issue_date')
        widgets = {
            'topic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of topic'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'doc_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
            'doc_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
            'topic2department': forms.Select(attrs={'class': 'form-control'}),
            'topic2company': forms.Select(attrs={'class': 'form-control'}),
        }

    # def clean_doc_file(self):
    #     docs = self.cleaned_data.get('doc_file')
    #     for doc in docs:
    #         if len(doc) > 100:
    #             raise ValidationError(_("Length of filename max 100 chars!"), code="length_error_file")
    #         return docs
    #
    # def clean_doc_image(self):
    #     docs = self.cleaned_data.get('doc_image')
    #     for doc in docs:
    #         if len(doc) > 100:
    #             raise ValidationError(_("Length of filename max 100 chars!"), code="length_error_image")
    #         return docs


class UpdateTopicsForm(forms.ModelForm):
    problem_info = forms.CharField(widget=CKEditorWidget(config_name='default'))
    action = forms.CharField(widget=CKEditorWidget(config_name='default'))

    class Meta:
        model = Topic
        fields = "__all__"
        exclude = ('topic2meeting', 'topic2user', 'status', 'new_due_date')
        widgets = {
            'topic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of topic'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'doc_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
            'doc_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
            'topic2department': forms.Select(attrs={'class': 'form-control'}),
            'topic2company': forms.Select(attrs={'class': 'form-control'}),
        }


class MultiUploadFileForm(forms.ModelForm):
    class Meta:
        model = TopicFile
        fields = ('doc_file',)
        widgets = {
            'doc_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True})
        }


class EntryActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"
        exclude = ('activity2topic', 'activity2user', 'activity_date')
        widgets = {
            'action_short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'action_description': forms.Textarea(attrs={'class': 'form-control'}),
            'activity_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'disabled': True},
                                             format='%Y-%m-%d'),
        }


class MultiUploadActivityFileForm(forms.ModelForm):
    class Meta:
        model = ActivityFile
        fields = ('doc_file',)
        widgets = {
            'doc_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True})
        }


class TopicActivityForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('problem_info', 'action', 'due_date', 'new_due_date', 'status')
        widgets = {
            'new_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                            format='%Y-%m-%d')
        }


class UpdateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('action_short_description', 'action_description')
        widgets = {
            'action_short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'action_description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class NewExternalParticipantForm(forms.ModelForm):
    class Meta:
        model = Outside
        fields = "__all__"
        exclude = ("outside2meeting",)
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'company_from': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
        }


class InputBulkUserForm(forms.Form):
    isi_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
