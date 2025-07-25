from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import Team


class  CustomRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'email')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'location', 'postal_code', 'rating')



class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'moto', 'description')

