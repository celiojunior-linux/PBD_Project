from django.contrib.auth.backends import ModelBackend

from apps.inventory.models import Employee


class EmployeeBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        document = kwargs["username"]
        password = kwargs["password"]
        try:
            employee = Employee.objects.get(document=document, password=password)
            # if customer.user.check_password(password) is True:
            #     return customer.user
            return employee
        except Employee.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            e = Employee.objects.get(pk=user_id)
            return e
        except Employee.DoesNotExist:
            return None
