from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import render, redirect


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get('confirmar_senha')
        users = User.objects.filter(username=username)

        if users.exists():
            print('Erro 1')
            messages.add_message(request, constants.ERROR, "Este usuario já existe")
            return redirect('/usuarios/cadastro')

        if senha != confirmar_senha:
            print('Erro 2')
            messages.add_message(request, constants.ERROR, "A senha e o confirmar senha diferentes")
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            print('Erro 3')
            messages.add_message(request, constants.ERROR, "A senha deve ter no mínimo 6 caracteres")
            return redirect('/usuarios/cadastro')

        users = User.objects.filter(username=username)

        if users.exists():
            redirect('/usuarios/cadtro')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )

            return redirect('/usuarios/login')
        except:
            print('Erro 4')
            messages.add_message(request, constants.ERROR, "Falha no sistema, tente outra vez")
            return redirect('/usuarios/cadastro')


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get("senha")
        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/pacientes/home')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
            return redirect('/usuarios/login')


def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')
