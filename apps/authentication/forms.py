from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

from apps.inventory.models import Company


class AMLAuthenticationForm(AuthenticationForm):

    company = forms.CharField(
        widget=forms.Select(
            attrs={"class": "form-control", "style": "border-radius:20px;"})
    )

    captcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
        widget=ReCaptchaV2Checkbox()
    )

    def __init__(self, *args, **kwargs):
        super(AMLAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields["company"].widget.choices = [(company.pk, company) for company in Company.objects.all()]
