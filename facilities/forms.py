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
    class Meta(BaseFacilityForm.Meta):
        fields = ('name', 'location', 'postcode', 'status', 'description')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['status'].disabled = True

        if user != self.instance.owner:
            for field in self.fields:
                self.fields[field].disabled = True


class DeleteFacilityForm(BaseFacilityForm):
    ...


class RemoveTenantForm(forms.ModelForm):
    tenant_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Facility
        fields = ('tenant_id',)
