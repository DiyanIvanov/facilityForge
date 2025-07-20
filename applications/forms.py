from django import forms
from django.db.models import Q
from django.apps import apps
from applications.models import Applications


class ApplicationForm(forms.Form):
    application_id = forms.IntegerField()
    action = forms.ChoiceField(
        choices=[
            ('accept', 'Accept'),
            ('reject', 'Reject')
        ],
    )


class TeamApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ('description',)



class FacilityApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ('description', 'team')


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['team'].queryset = apps.get_model('accounts', 'Team').objects.filter(
                Q(team_owner=user) | Q(manager=user)
            ).distinct()
            self.fields['team'].required = False
            self.fields['team'].label = "Apply as team (optional)"
            self.fields['team'].widget.attrs.update({'class': 'form-select'})
