from django.db.models import Manager, Q


class TicketManager(Manager):
    def open_tickets(self):
        return self.filter(status='open')

    def in_progress_tickets(self):
        return self.filter(status='in_progress')

    def completed_tickets(self):
        return self.filter(status='completed')

    def closed_tickets(self):
        return self.filter(status='closed')

    def get_all_user_tickets(self, user):
        return self.filter(
            (Q(created_from=user) |
            Q(facility__manager=user) |
            Q(facility__owner=user) |
            Q(assigned_to__manager=user) |
            Q(assigned_to__members=user)) &
            Q(status__in=['open', 'in_progress', 'completed'])
        ).distinct()
