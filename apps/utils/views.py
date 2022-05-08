from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView

MESSAGE_DELETED_SUCCESSFULLY = "Registro de %s eliminado com sucesso!"


class BetterDeleteView(DeleteView):
    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, MESSAGE_DELETED_SUCCESSFULLY % self.model._meta  .verbose_name.capitalize())
        except ProtectedError:
            messages.warning(
                self.request,
                f"Não foi possível deletar o registro de {self.object} \
                pois ele está sendo usado em outros registros.",
            )
        return HttpResponseRedirect(success_url)
