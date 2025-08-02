from django.views.generic import DeleteView
from django.contrib import messages
from django.shortcuts import redirect


class DeleteObjectMixin(DeleteView):
    message = 'This object cannot be delete at that time.'
    fail_url = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tickets.filter(status__in=['open', 'in_progress']).exists():
            messages.warning(self.request, self.message)

            if not self.fail_url:
                return redirect('index')

            return redirect(self.fail_url, pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)
