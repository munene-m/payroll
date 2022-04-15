from operator import le
from webbrowser import get
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from .models import Employee, Leave
from .forms import *

# Create your views here.
class Dashboard(ListView):
    template_name = 'shop/employees/employees.html'
    model = Employee
    context_object_name = 'qset'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['emp_total'] = Employee.objects.all().count()
        context['employees'] = Employee.objects.order_by('-id')
        return context

class Employee_Update(LoginRequiredMixin,UpdateView):
    model = Employee
    template_name = 'shop/employees/update.html'
    form_class = EmployeeUpdateForm
    success_url =reverse_lazy('shop:dashboard')

def signupview(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')  
            return redirect('shop:dashboard')
    else:
        form = EmployeeCreationForm()
    return render(request, 'shop/employees/register.html', {'form': form})

class Leaves(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
            form = LeaveForm()
            context = {
                "form": form,
            }
            return render(self.request, 'shop/employees/leaves.html', context)
    
    def post(self, *args, **kwargs):
        form = LeaveForm(self.request.POST or None)
        employee= self.request.user
        applicant= Employee.objects.get(user=employee)

        print('Employee : ', employee)
        print('Applicant : ', applicant)

        if form.is_valid():
            start_date=form.cleaned_data.get("start")
            end_date=form.cleaned_data.get("end")
            reason=form.cleaned_data.get("reason")

            leave=Leave(
                employee = applicant,
                start=start_date,
                end=end_date,
                reason=reason
            )
            leave.save()
            messages.success(self.request, "successfully submitted request")
            return redirect("shop:leave-list")
        messages.warning(self.request, "Failed Process")
        return redirect("shop:leave-list")

class Leave_List(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'shop/employees/leave_list.html'

class Leave_Update(LoginRequiredMixin,UpdateView):
    model = Leave
    template_name = 'shop/employees/approve.html'
    form_class = LeaveUpdateForm
    success_url =reverse_lazy('shop:leave-list')


class Pay(LoginRequiredMixin,ListView):
    model = Employee
    template_name = 'shop/employees/payroll.html'
    context_object_name = 'employees'
