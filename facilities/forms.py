from django.forms import ModelForm


class BaseFacilityForm(ModelForm):

    class Meta:
        model = 'facilities.Facility'
        fields = '__all__'



class CreateFacilityForm(BaseFacilityForm):

    class Meta(BaseFacilityForm.Meta):
        fields = ['name', 'description', 'location', 'postcode']


class UpdateFacilityForm(BaseFacilityForm):

    ...

class DeleteFacilityForm(BaseFacilityForm):
    ...
