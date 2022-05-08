from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


class AMLAuthenticationForm(AuthenticationForm):

    if settings.DEBUG is False:
        captcha = ReCaptchaField(
            public_key=settings.RECAPTCHA_PUBLIC_KEY,
            private_key=settings.RECAPTCHA_PRIVATE_KEY,
            widget=ReCaptchaV2Checkbox()
        )
