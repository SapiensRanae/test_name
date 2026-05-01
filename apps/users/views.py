from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import CustomUserCreationForm, CustomUserUpdateForm, UserProfileForm
from .models import CustomUser

from apps.core.models import QuizAttempt



class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect('welcome')


class UsersView(View):
    def get(self, request):
        # Check if user is admin
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('welcome')
        
        user_list = CustomUser.objects.all()
        user_form_list = [CustomUserUpdateForm(instance=user, prefix=str(i)) for i, user in enumerate(user_list)]
        return render(request, 'users/users.html', {
            'user_form_list': user_form_list,
        })

    def post(self, request):
        # Check if user is admin
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('welcome')
        
        if 'submit_user_update' in request.POST:
            prefix = request.POST.get('submit_user_update')
            user_list = CustomUser.objects.all()
            user = user_list[int(prefix)]
            user_form = CustomUserUpdateForm(request.POST, instance=user, prefix=prefix)
            if user_form.is_valid():
                user_form.save()
                return redirect('users')
        user_list = CustomUser.objects.all()
        user_form_list = [CustomUserUpdateForm(instance=user, prefix=str(i)) for i, user in enumerate(user_list)]
        return render(request, 'users/users.html', {
            'user_form_list': user_form_list,
        })


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        profile = getattr(request.user, 'profile', None)
        form = UserProfileForm(instance=profile) if profile else UserProfileForm()
        return render(request, 'users/profile.html', {
            'profile': profile,
            'form': form
        })


class MyAttemptsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        attempts = QuizAttempt.objects.filter(user=request.user, submittedAt__isnull=False).select_related('quiz').order_by('-submittedAt')
        return render(request, 'users/my_attempts.html', {
            'attempts': attempts,
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        profile = getattr(request.user, 'profile', None)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
        return render(request, 'users/profile.html', {
            'profile': profile,
            'form': form
        })

