from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from .forms import EmailAuthenticationForm, PatientRegisterForm
from .models import RoleChoices

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = EmailAuthenticationForm

    def get_success_url(self):
        user = self.request.user
        if user.role == RoleChoices.ADMIN:
            return '/admin/'
        if user.role == RoleChoices.DOCTOR:
            return '/doctor/'
        return '/profile/'

    def form_invalid(self, form):
        messages.error(self.request, 'Невірний email або пароль.')
        return super().form_invalid(form)


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = PatientRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('profile')
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    if request.user.role == RoleChoices.ADMIN:
        return redirect('/admin/')
    if request.user.role == RoleChoices.DOCTOR:
        return redirect('doctor_dashboard')
    return redirect('profile')
