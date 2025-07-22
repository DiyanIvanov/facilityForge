from django.db.models import Q
from django.forms import ModelForm
from tickets.models import Tickets
from django.apps import apps

class BaseTicketForm(ModelForm):
    class Meta:
        model = Tickets
        fields = '__all__'


class CreateTicketForm(BaseTicketForm):
    class Meta(BaseTicketForm.Meta):
        fields = ['title', 'facility', 'priority', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['facility'].queryset = apps.get_model('facilities', 'Facility').objects.filter(
                Q(owner=user) | Q(manager=user) | Q(tenants=user)
            ).distinct()


class UpdateTicketForm(BaseTicketForm):
    ...