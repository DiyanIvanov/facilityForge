from django import forms

class ApplicationForm(forms.Form):
    application_id = forms.IntegerField()
    action = forms.ChoiceField(
        choices=[
            ('accept', 'Accept'),
            ('reject', 'Reject')
        ],
    )
