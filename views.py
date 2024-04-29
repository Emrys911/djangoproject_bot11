
from django.contrib.auth import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm()
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm()
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def chat(request):
    # Обработка запросов чата
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        # Здесь можно передать вход пользователя в модель GPT и получить ответ
        bot_response = "Привет! Я чат-бот."
        return JsonResponse({'bot_response': bot_response})
    else:
        return render(request, 'chat.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


def register_user(request):
    return ('/')
