from django.views.generic import UpdateView

from apps.inventory import models, forms
from apps.utils import mixins


class CompanyEditView(UpdateView, mixins.ModelUpdateMixin):
    model = models.Company
    template_name = "system/company_settings.html"
    form_class = forms.CompanyForm

    def get_object(self, queryset=None):
        return models.Company.object()


    def get_success_url(self):
        return self.request.path
