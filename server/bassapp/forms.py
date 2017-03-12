from django import forms
from django.contrib.auth import get_user_model

from bassapp.models import Project


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=False)


class ProjectDataForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('id', 'user', 'likes', 'data_public')


class GetProjectForm(forms.Form):
    id = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        help_text="Project ID"
    )


class ProjectVoteForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        help_text="Project ID"
    )
    value = forms.BooleanField(required=False)


class SubscribeForm(forms.Form):
    author = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        help_text="User ID"
    )
    value = forms.BooleanField(required=False)


class UserProjectsForm(forms.Form):
    author = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        help_text="User ID"
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'avatar')
