from django import forms
from django.contrib.auth.models import User
from users_register_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    # Edit password field (if we don't edit, it will be a plaint text only)
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    # We don't have to edit nothing here...
    class Meta(): # Meta class is treated as a constructor
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
