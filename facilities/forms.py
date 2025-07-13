from django.forms import ModelForm
from django import forms
from facilities.models import Facility


class BaseFacilityForm(ModelForm):

    class Meta:

        model = Facility
        fields = '__all__'



class CreateFacilityForm(BaseFacilityForm):

    class Meta(BaseFacilityForm.Meta):
        fields = ['name', 'description', 'location', 'postcode']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 128px;',
            }),
        }


class UpdateFacilityForm(BaseFacilityForm):

    ...

class DeleteFacilityForm(BaseFacilityForm):
    ...
