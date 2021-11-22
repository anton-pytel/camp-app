
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from camper.models import Child, ChildHealth, Parent, ChildParent


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Prihlasovacie meno",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Heslo",
                "class": "form-control"
            }
        ))


class RegisterChildForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Janko",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Hráško",
                "class": "form-control"
            }
        ))

    birth_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "010203/1234",
                "class": "form-control"
            }
        ))

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Táborova ulica 1/2",
                "class": "form-control"
            }
        ))

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Prievidza",
                "class": "form-control"
            }
        ))

    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "SK",
                "class": "form-control"
            }
        ))

    swim = forms.ChoiceField(choices=(
        (Child.SwimStatus.NO, "Nie"),
        (Child.SwimStatus.YES, "Áno"),
        (Child.SwimStatus.ABIT, "Trochu")
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        diseases = ChildHealth.objects.filter(
            child=self.instance
        )
        for i in range(len(diseases) + 1):
            field_name = 'disease_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = diseases[i].interest
            except IndexError:
                self.initial[field_name] = ""
                # create an extra blank field
                field_name = 'disease_%s' % (i + 1,)
                self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        diseases = set()
        i = 0
        field_name = 'disease_%s' % (i,)
        while self.cleaned_data.get(field_name):
            disease = self.cleaned_data[field_name]
            if disease in diseases:
                self.add_error(field_name, 'Duplicate')
            else:
                diseases.add(disease)
            i += 1
            field_name = 'disease_%s' % (i,)

        self.cleaned_data["diseases"] = diseases

    def save(self):
        child = self.instance
        child.first_name = self.cleaned_data["first_name"]
        child.last_name = self.cleaned_data["last_name"]

        child.interest_set.all().delete()
        for disease in self.cleaned_data["diseases"]:
            ChildHealth.objects.create(
                child=child,
                disease_name=disease,
                    )

    def get_disease_fields(self):
        for field_name in self.fields:
            if field_name.startswith('disease_'):
                yield self[field_name]

    class Meta:
        model = Child
        fields = [
            "birth_number",
            "address",
            "city",
            "state",
            "swim",
        ]


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Prihlasovacie meno",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Heslo",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Potvrdenie hesla",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
