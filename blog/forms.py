from django import forms
from django.contrib.auth.models import User
from .models import Post


class UserRegistrationForm(forms.ModelForm):
    """This is model form based on User model and lets user to register."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """Checks if second password matches the first one"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don`t match.')
        return cd['password2']


class AddPost(forms.ModelForm):
    """Model form based on model Post. Lets user to add post"""
    class Meta:
        model = Post
        fields = ('title', 'slug', 'body')


class EditPost(forms.Form):
    """This form lets user edit their posts"""
    title = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)


class SearchForm(forms.Form):
    """This form is for searching post via query-word.
        Returns posts with query_word in body or in title"""
    query = forms.CharField()
