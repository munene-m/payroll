from .models import Employee
from django.contrib.auth.models import User

def employee_count(request):
    if request.user.is_authenticated:
        employee_count= Employee.objects.all().count()
        users=User.objects.all().count()
        admin_count=users-employee_count

        return { 'employee_count':employee_count,
                    'admin_count':admin_count
                    }
    return { }

