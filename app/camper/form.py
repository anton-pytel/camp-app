
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from camper.models import Child, ChildHealth, Parent, ChildParent, Participant
from phonenumber_field.formfields import PhoneNumberField
from copy import deepcopy


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
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "0102031234",
                "class": "form-control"
            }
        ))

    date_birth = forms.DateField(
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                "class": "form-control datetimepicker",
                "type": "text",
                "placeholder": "dd.mm.yyyy",
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

    swim = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control"
            },
            choices=(
                (Child.SwimStatus.NO, "Neviem"),
                (Child.SwimStatus.YES, "Viem"),
            ),
        ),
    )

    p_first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Meno",
                "class": "form-control"
            }
        ))
    p_last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Priezvisko",
                "class": "form-control"
            }
        ))

    p_email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "meno.priezvisko@mail.sk",
                "class": "form-control"
            }
        )
    )
    p_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "+421 901 234 567",
                "class": "form-control"
            }
        )
    )
    p_number.error_messages['invalid'] = "Zadajte telefónne číslo v správnom tvare (napr. +421911 111 111)"

    consent_photo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
            }
        )
    )
    consent_agreement = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        diseases = []
        for itm in self.data:
            if itm.startswith('disease_'):
               data = self.data[itm]
               if data and len(data) > 0:
                   diseases.append(ChildHealth(disease_name=data))
        dis_i = 0
        help_txt = "".join((
            "Zadajte alergie, intolerancie, "
            "prípadne iné dôležité informácie. ",
            "Napíšte \"zdravý/á\", ak nie je nič, na čo by sme mali ",
            "v jedálničku a pri aktivitách dávať pozor.")
        )
        self.diseases = diseases
        for dis in diseases:
            field_name = f'disease_{dis_i}'

            self.fields[field_name] = forms.CharField(
                required=False,
                widget=forms.TextInput(
                    attrs={
                        "class": "form-control remove-empty",
                    }
                ),
                help_text=help_txt

            )
            help_txt = ''
            self.initial[field_name] = dis.disease_name
            setattr(dis, 'field_label_name', self[field_name])
            dis_i = dis_i + 1
        field_name = f'disease_{dis_i}'
        dis = ChildHealth()
        self.fields[field_name] = forms.CharField(
            required=False,
            widget=forms.TextInput(
                attrs={
                    "class": "form-control disease_new remove-empty",
                }
            ),
            help_text=help_txt
        )
        setattr(dis, 'field_label_name', self[field_name])
        self.diseases.append(dis)

        # for i in range(len(diseases) + 1):
        #     field_name = 'disease_%s' % (i,)
        #     self.fields[field_name] = forms.CharField(
        #         required=False,
        #         widget=forms.TextInput(
        #             attrs={
        #                 "class": "form-control disease_new",
        #             }
        #         ),
        #         help_text="".join((
        #             "Zadajte alergie, intolerancie, "
        #             "prípadne iné dôležité informácie. ",
        #             "Napíšte \"zdravý/á\", ak nie je nič, na čo by sme mali ",
        #             "v jedálničku a pri aktivitách dávať pozor.")
        #         )
        #     )
        #     try:
        #         self.initial[field_name] = diseases[i].disease_name
        #     except IndexError:
        #         self.initial[field_name] = ""
        #         # create an extra blank field
        #         field_name = 'disease_%s' % (i + 1,)
        #         self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        diseases = set()
        i = 0
        field_name = 'disease_%s' % (i,)
        while self.cleaned_data.get(field_name):
            disease = self.cleaned_data[field_name]
            if disease in diseases:
                self.add_error(field_name, 'Duplicita')
            else:
                diseases.add(disease)
            i += 1
            field_name = 'disease_%s' % (i,)
        if len(diseases) == 0:
            self.add_error("disease_0", "Zdravotný stav musí byť vyplnený")
        self.cleaned_data["diseases"] = diseases

    def save(self):
        child = self.instance
        child.first_name = self.cleaned_data["first_name"]
        child.last_name = self.cleaned_data["last_name"]

        child.childhealth_set.all().delete()
        for disease in self.cleaned_data["diseases"]:
            ChildHealth.objects.create(
                child=child,
                disease_name=disease,
                    )

    def get_diseases(self):
        return self.diseases

    def get_disease_fields(self):
        for field_name in self.fields:
            if field_name.startswith('disease_'):
                yield self[field_name]

    class Meta:
        model = Child
        fields = [
            "birth_number",
            "date_birth",
            "address",
            "city",
            "state",
            "swim",
        ]


class ProfileForm(forms.ModelForm):

    p_first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Meno",
                "class": "form-control"
            }
        ))
    p_last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Priezvisko",
                "class": "form-control"
            }
        ))

    p_email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "meno.priezvisko@mail.sk",
                "class": "form-control"
            }
        )
    )
    p_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "+421 901 234 567",
                "class": "form-control"
            }
        )
    )
    p_number.error_messages['invalid'] = "Zadajte telefónne číslo v správnom tvare (napr. +421911 111 111)"

    def __init__(self, *args, **kwargs):
        def get_diseases(self):
            return self.diseases

        def get_participation(self):
            return self.participation

        setattr(Child, 'get_diseases', get_diseases)
        setattr(Child, 'get_participation', get_participation)
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.children = []
        if self.request.user.is_authenticated:
            try:
                p = Parent.objects.get(user=self.request.user)
                self.parent = p
                self.children = list(Child.objects.filter(childparent__parent=p))

                self.initial["p_first_name"] = p.user.first_name
                self.initial["p_last_name"] = p.user.last_name
                self.initial["p_number"] = p.contact_phone
                self.initial["p_email"] = p.contact_email
                i_idx = 0
                reg_form = RegisterChildForm()
                for ch in self.children:
                    idx = str(i_idx)
                    for itm in ["first_name", "last_name"]:
                        self.fields[itm + "_" +idx] = deepcopy(reg_form.fields[itm])
                        self.initial[itm + "_" + idx] = getattr(ch.user, itm)
                        setattr(ch, "field_" + itm, self[itm + "_" + idx])
                    for itm in ["date_birth", "address", "city", "state", "swim"]:
                        self.fields[itm + "_" + idx] = deepcopy(reg_form.fields[itm])
                        self.initial[itm + "_" +idx] = getattr(ch, itm)
                        setattr(ch, "field_" + itm, self[itm + "_" + idx])
                    ch.idx = i_idx
                    diseases = list(ch.childhealth_set.all())
                    ch.diseases = diseases
                    ch.participation = list(ch.participant_set.filter(valid_participant=True))
                    for p in ch.participation:
                        p.price_diff = p.price - p.advance_price
                    ch.part_len = len(ch.participation)
                    dis_i = 0
                    for dis in diseases:
                        field_name = f'disease_{i_idx}_{dis_i}'
                        self.fields[field_name] = forms.CharField(
                            required=False,
                            widget=forms.TextInput(
                                attrs={
                                    "class": "form-control remove-empty",
                                }
                            )
                        )
                        self.initial[field_name] = dis.disease_name
                        setattr(dis, 'field_label_name', self[field_name])
                        dis_i = dis_i + 1
                    field_name = f'disease_{i_idx}_{dis_i}'
                    dis = ChildHealth()
                    self.fields[field_name] = forms.CharField(
                        required=False,
                        widget=forms.TextInput(
                            attrs={
                                "class": "form-control disease_new remove-empty",
                            }
                        )
                    )
                    setattr(dis, 'field_label_name', self[field_name])
                    ch.diseases.append(dis)

                    i_idx = i_idx + 1
            except Parent.DoesNotExist:
                pass

    def get_children(self):
        return self.children

    class Meta:
        model = Participant
        fields = [
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
