from django import forms
from django.contrib.auth import get_user_model
from django.contrib.postgres.forms import SimpleArrayField

from .models import Project


class ArrayField(SimpleArrayField):
    def to_python(self, value):
        if isinstance(value, list):
            return value
        return super(ArrayField, self).to_python(value)

# class AppDataField(forms.CharField):
#     def clean(self, value):
#         pass


class ProjectDataForm(forms.ModelForm):
    # data = AppDataField(required=False)

    def full_clean(self):
        current_data = self.instance.data if self.instance else None
        # when 'data' was not explicitly passed, do not modify it
        if 'data' not in self.data:
            self.fields.pop('data')
        super(ProjectDataForm, self).full_clean()

    class Meta:
        model = Project
        exclude = ('id', 'user', 'likes', 'data_public')
        field_classes = {
            'genres': ArrayField,
            'playing_styles': ArrayField,
            'tags': ArrayField,
            'tracks': ArrayField
        }


class GetProjectForm(forms.Form):
    id = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        help_text="Project ID"
    )
    data = forms.BooleanField(required=False)


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
        fields = ('first_name', 'last_name', 'email', 'avatar', 'links')
