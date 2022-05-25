from django.contrib.auth.backends import ModelBackend

from apps.inventory.models import Employee, Company


class EmployeeBackend(ModelBackend):

    @staticmethod
    def authenticate(request, **kwargs):
        document = kwargs["username"]
        password = kwargs["password"]
        company = request.POST["company"]
        try:
            president = request.headquarter.president
            if president:
                if president.document == document and president.password == password:
                    president.company = Company.objects.get(pk=company)
                    president.save()
                    return president
            employee = Employee.objects.get(document=document, password=password, company=company)
            return employee
        except Employee.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            e = Employee.objects.get(pk=user_id)
            return e
        except Employee.DoesNotExist:
            return None
