from django.shortcuts import render, redirect
from .forms import UserLoginForm, CustomUserCreationForm
from django.contrib import auth


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:chat')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return redirect('users:chat')
            else:
                form.add_error(None, "Invalid email or password.")

        else:
            form.add_error(None, "Invalid email or password.")

    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.user.is_authenticated:
        return redirect('users:chat')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/registration.html', {'form': form})
