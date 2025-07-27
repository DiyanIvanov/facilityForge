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


class BaseTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'moto', 'description', 'members', 'team_owner')


class CreateTeamForm(BaseTeamForm):
    class Meta(BaseTeamForm.Meta):
        fields = ('name', 'moto', 'description')


class EditTeamForm(BaseTeamForm):
    class Meta(BaseTeamForm.Meta):
        ...

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user != self.instance.team_owner:
            for field in self.fields:
                self.fields[field].disabled = True





class RemoveMemberForm(forms.ModelForm):
    member_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Team
        fields = ('member_id',)