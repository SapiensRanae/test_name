from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser



class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class UsersView(View):
    def get(self, request):
        user_list = CustomUser.objects.all()
        user_form_list = [CustomUserUpdateForm(instance=user, prefix=str(i)) for i, user in enumerate(user_list)]
        return render(request, 'users/users.html', {
            'user_form_list': user_form_list,
        })

    def post(self, request):
        # !!!!!! Для отримання файлу з форми request.FILES
        # client_form = ClientForm(request.POST, request.FILES, instance=client, prefix='client')
        if 'submit_user_update' in request.POST:
            prefix = request.POST.get('submit_user_update')
            user_list = CustomUser.objects.all()
            user = user_list[int(prefix)]

            user_form = CustomUserUpdateForm(request.POST, instance=user, prefix=prefix)
            if user_form.is_valid():
                user_form.save()
                return redirect('users')
            else:
                print(user_form.errors)

        user_list = CustomUser.objects.all()
        user_form_list = [CustomUserUpdateForm(instance=user, prefix=str(i)) for i, user in enumerate(user_list)]
        return render(request, 'users/users.html', {
            'user_form_list': user_form_list,
        })
