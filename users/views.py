from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Акаунт {username} успішно створено! Тепер ви можете увійти.')
            return redirect('login')
        else:
            messages.error(request, 'Помилка при реєстрації. Будь ласка, перевірте дані.')
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html', {'form': form})