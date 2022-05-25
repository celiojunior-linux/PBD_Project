from apps.inventory.models import Company


class CompanyMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.headquarter = Company.get_current_headquarter()
        return self.get_response(request)
