from django import forms
from applications.models import Applications


class ApplicationForm(forms.Form):
    application_id = forms.IntegerField()
    action = forms.ChoiceField(
        choices=[
            ('accept', 'Accept'),
            ('reject', 'Reject')
        ],
    )


class TeamOrFacilityApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ('description',)

