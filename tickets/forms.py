from django.db.models import Q
from django.forms import ModelForm
from tickets.models import Tickets, TicketMessages
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
    class Meta(BaseTicketForm.Meta):
        fields = ['id', 'title', 'facility', 'status', 'priority', 'description', 'assigned_to']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['facility'].disabled = True

        if self.instance.facility.owner != user \
            or self.instance.assigned_to.members == user or self.instance.assigned_to.team_owner == user:
            self.fields['status'].disabled = True
            self.fields['assigned_to'].disabled = True



class TicketMessageForm(ModelForm):
    class Meta:
        model = TicketMessages
        fields = ['content']

