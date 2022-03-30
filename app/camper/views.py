from unidecode import unidecode
from datetime import datetime, timedelta
from django import template
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    PasswordResetForm
)
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings

from camper.form import (
    LoginForm, RegisterUserForm, RegisterChildForm,
    ProfileForm
)
from camper.utils import generate_random_password, get_username, filter_f_l_name
from camper.models import (
    Child, Parent, Participant, ChildHealth, ChildParent,
    Registration
)

# Create your views here.


def index(request):
    context = {
        'segment': 'index'
    }

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    #try:

    load_template = request.path.split('/')[-1]
    context['segment'] = load_template

    html_template = loader.get_template(load_template)
    return HttpResponse(html_template.render(context, request))

    #except template.TemplateDoesNotExist:

    #    html_template = loader.get_template('page-404.html')
    #    return HttpResponse(html_template.render(context, request))

    #except:
    #    html_template = loader.get_template('page-500.html')
    #    return HttpResponse(html_template.render(context, request))


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
                return redirect("/")
            else:
                msg = 'Neplatné prihlasovacie údaje'
        else:
            msg = 'Chyba pri validácii'
    return render(request, "accounts/login.html", {"form": form, "msg": msg, 'segment': 'login'})


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    form = ProfileForm(request.POST or None, request=request)
    msg = None
    success = False

    if request.method == "POST":
        if 'delete-btn' in request.POST:
            child_id = request.POST["delete-btn"]
            msg = "Záznam vymazaný"
            Child.objects.filter(id=child_id).delete()
            form = ProfileForm(None, request=request)
        elif 'delete-part-btn' in request.POST:
            part_id = request.POST["delete-part-btn"]
            msg = "Záznam vymazaný"
            Participant.objects.filter(id=part_id).delete()
            form = ProfileForm(None, request=request)
        elif 'register-btn' in request.POST:
            child_id = request.POST["register-btn"]
            msg = "Účastník zaregistrovaný"
            registration = Registration.objects.get(
                label=settings.VALID_REGISTRATION
            )
            child = Child.objects.get(id=child_id)
            particip, is_new = Participant.objects.get_or_create(
                registration=registration,
                child=child,
                defaults={
                    "price": registration.price,
                    "advance_price": registration.advance_price
                }
            )
            particip.confirm_mail(settings.PAGE_DOMAIN)
            due_dt = datetime.now() + timedelta(settings.ADVANCE_PMT_DUE) # +day
            particip.generate_qr(due_dt)
            form = ProfileForm(None, request=request)
        elif form.is_valid():
            p = form.parent
            p.contact_email = form.cleaned_data.get("p_email")
            p.contact_phone = form.cleaned_data.get("p_number").as_international
            p.user.first_name = form.cleaned_data.get("p_first_name")
            p.user.last_name = form.cleaned_data.get("p_last_name")
            p.user.email = form.cleaned_data.get("p_email")
            p.user.save()
            p.save()
            for child in form.children:
                idx = str(child.idx)
                child.user.first_name = form.cleaned_data.get("first_name_"+idx)
                child.user.last_name = form.cleaned_data.get("last_name_" + idx)
                # child.birth_number = form.cleaned_data.get("birth_number_" + idx)
                child.date_birth = form.cleaned_data.get("date_birth_" + idx)
                child.address = form.cleaned_data.get("address_" + idx)
                child.city = form.cleaned_data.get("city_" + idx)
                child.state = form.cleaned_data.get("state_" + idx)
                child.swim = form.cleaned_data.get("swim_" + idx)
                ChildHealth.objects.filter(child=child).delete()
                child.save()
                for key in form.data.items():
                    if 'disease_' + str(idx) + '_' in key[0]:
                        label = form.data.get(key[0])
                        if label:
                            ChildHealth.objects.create(
                                child=child,
                                disease_name=label
                            )

            form = ProfileForm(None, request=request)
            msg = "Zmeny uložené"

        else:
            msg = "Skontrolujte vstupné dáta"

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "msg": msg,
            "iban": settings.VALID_IBAN,
            "success": success,
            "segment": "profile"
        }
    )


def register_child_view(request):
    form = RegisterChildForm(request.POST or None)
    parent = None
    if request.user.is_authenticated:
        try:
            parent = Parent.objects.get(user=request.user)
            form.initial["p_first_name"] = parent.user.first_name
            form.initial["p_last_name"] = parent.user.last_name
            form.initial["p_email"] = parent.contact_email
            form.initial["p_number"] = parent.contact_phone
        except Parent.DoesNotExist:
            pass
    msg = None
    success = False
    success_msg = ""

    if request.method == "POST":

        if form.is_valid():
            # vytvorit dieta (vygenerovat heslo a username)
            # vytvorenie rodica ak rovnaky email priradit dieta k tomu istemu
            # prihlasenie do platnej registracie
            try:
                due_dt = datetime.now() + timedelta(settings.ADVANCE_PMT_DUE)  # +days
                registration = Registration.objects.get(
                    label=settings.VALID_REGISTRATION
                )
                child = Child.objects.filter(
                    date_birth=form.cleaned_data.get("date_birth")
                )
                child = filter_f_l_name(
                    child,
                    form.cleaned_data.get("first_name"),
                    form.cleaned_data.get("last_name")
                )
                sfx1 = generate_random_password(3).lower()
                sfx2 = generate_random_password(3).lower()
                participation = []
                child_exists = False
                if len(child) > 0:
                    child = child[0]
                    participation = Participant.objects.filter(
                        child=child,
                        registration=registration
                    )
                    u_child = child.user
                    child_exists = True
                else:
                    c_pass = generate_random_password(8)

                    u_child = User.objects.create_user(
                        first_name=form.cleaned_data.get("first_name"),
                        last_name=form.cleaned_data.get("last_name"),
                        username=get_username(
                            form.cleaned_data.get("first_name"),
                            form.cleaned_data.get("last_name"),
                            sfx1
                        ),
                        password=c_pass,
                    )

                if len(participation) > 0:
                    msg = "Účastník je už registrovaný"
                else:
                    p_pass = generate_random_password(8)
                    p_created = False
                    if not parent:
                        try:
                            u_parent = User.objects.get(email=form.cleaned_data.get("p_email"))
                        except User.DoesNotExist:
                            u_parent = User.objects.create_user(
                                email=form.cleaned_data.get("p_email"),
                                first_name=form.cleaned_data.get("p_first_name"),
                                last_name=form.cleaned_data.get("p_last_name"),
                                username=get_username(
                                    form.cleaned_data.get("p_first_name"),
                                    form.cleaned_data.get("p_last_name"),
                                    sfx2
                                ),
                                password=p_pass,
                            )
                            p_created = True

                        if p_created:
                            parent = Parent.objects.create(
                                user=u_parent,
                                contact_phone=form.cleaned_data.get("p_number").as_international,
                                contact_email=form.cleaned_data.get("p_email"),
                            )
                            login(request, u_parent)
                        else:
                            parent = Parent.objects.get(user=u_parent)

                    if child_exists:
                        child.address = form.cleaned_data.get("address")
                        child.city = form.cleaned_data.get("city")
                        child.state = form.cleaned_data.get("state")
                        child.swim = form.cleaned_data.get("swim")
                        child.save()
                    else:
                        child = Child.objects.create(
                            date_birth=form.cleaned_data.get("date_birth"),
                            user=u_child,
                            address=form.cleaned_data.get("address"),
                            city=form.cleaned_data.get("city"),
                            state=form.cleaned_data.get("state"),
                            swim=form.cleaned_data.get("swim"),
                        )
                    for key in form.data.items():
                        if 'disease_' in key[0]:
                            label = form.data.get(key[0])
                            if label:
                                ChildHealth.objects.get_or_create(
                                    disease_name=label,
                                    child=child
                                )
                    ChildParent.objects.get_or_create(
                        parent=parent,
                        child=child
                    )
                    participation, is_new = Participant.objects.get_or_create(
                        registration=registration,
                        child=child,
                        defaults={
                            "price": registration.price,
                            "advance_price": registration.advance_price,
                            "consent_photo": form.cleaned_data.get("consent_photo"),
                            "consent_agreement": form.cleaned_data.get("consent_agreement"),
                        }
                    )
                    participation.generate_qr(due_dt)
                    participation.confirm_mail(settings.PAGE_DOMAIN)
                    success_msg = '<div class="alert alert-success">Účastník úspešne zaregistrovaný</div>'
                    success = True
                    if p_created:
                        success_msg = success_msg + \
                                      f'<div class="alert alert-success">Rodičovský profil vytvorený, ' + \
                                      f'<ul><li>prihlasovacie meno: ' + \
                                      f'<span class="text-primary">{parent.user.username}</span</li>' + \
                                      f'<li>heslo: <span class="text-primary">{p_pass}</span></li>' + \
                                      f'<li>Prihlasovacie údaje si uložte, heslo si môžete zmeniť ' + \
                                      f'<a href="{reverse("password_change")}" class="text-primary">tu</a></li>' + \
                                      f'<li>Údaje o registrácii je možné skontrolovať ' + \
                                      f'<a href="{reverse("profile")}" class="text-primary" >tu</a></li></ul></div>'

                    success_msg = mark_safe(success_msg)

            except Registration.DoesNotExist:
                msg = "Aplikácia nie je pripravená na používanie, kontaktujte administrátora"
        else:
            msg = 'Nesprávne zadané údaje - skontrolujte všetky záložky'
    return render(
        request,
        "accounts/register_child.html",
        {
            "form": form,
            "msg": msg,
            "success": success,
            "success_msg": success_msg,
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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Žiadosť o zmenu hesla"
                    email_template_name = "pass_reset/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': settings.PAGE_DOMAIN,
                        'site_name': 'Tábor 2022',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        if settings.EMAIL_ENABLED:
                            send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Nepodarilo sa poslať')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="pass_reset/password_reset.html",
                  context={"password_reset_form": password_reset_form})

