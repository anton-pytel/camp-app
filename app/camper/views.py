from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from camper.form import (
    LoginForm, RegisterUserForm, RegisterChildForm,
    ProfileForm
)

# Create your views here.


def index(request):
    context = {
        'segment': 'index'
    }

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/camp")
            else:
                msg = 'Neplatné prihlasovacie údaje'
        else:
            msg = 'Chyba pri validácii'
    return render(request, "accounts/login.html", {"form": form, "msg": msg, 'segment': 'login'})


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    form = ProfileForm(request=request)
    msg = None
    success = False

    if request.method == "POST":
        # TODO: add/remove child
        #
        pass

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "msg": msg,
            "success": success,
            "segment": "profile"
        }
    )

def register_child_view(request):
    form = RegisterChildForm(request.POST or None)
    msg = None
    success = False

    if request.method == "POST":

        if form.is_valid():
            # TODO: spracovanie
            # vytvorit dieta (vygenerovat heslo a username)
            # vytvorenie rodica ak rovnaky email priradit dieta k tomu istemu
            # prihlasenie do platnej registracie
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/profile")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Nesprávne zadané údaje'
    return render(
        request,
        "accounts/register_child.html",
        {
            "form": form,
            "msg": msg,
            "success": success,
            "segment": "register-child"
        }
    )


def register_user_view(request):
    msg = None
    success = False

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Registrácia úspešná'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Formulár nie je platný'
    else:
        form = RegisterUserForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "msg": msg,
            "success": success,
            "segment": "register"
        }
    )
