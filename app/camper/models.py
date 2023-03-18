import logging
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from .utils import get_qr


logger = logging.getLogger("camper")


def validate_rc(value):
    try:
        num = int(value)
        p1 = num % 11 == 0
        m = int(value[2:4])
        if m > 50:
            m = m - 50
        if not (1 <= m <= 12 and len(value) == 10 and p1):
            raise
    except Exception:
        raise ValidationError(
            _('Neplatné rodné číslo'),
        )


class Registration(models.Model):
    label = models.CharField(default=settings.VALID_REGISTRATION, max_length=100)
    registration_start = models.DateField()
    registration_end = models.DateField()
    camp_start_date = models.DateField()
    camp_start_end = models.DateField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=5)
    advance_price = models.DecimalField(max_digits=20, decimal_places=2, default=3)
    bank_account = models.CharField(default=settings.VALID_IBAN, max_length=100)

    def __str__(self):
        return self.label


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_phone = models.CharField(max_length=17)
    contact_email = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parent'

    def __str__(self):
        return f'parent: {self.user.last_name} {self.user.first_name}'


class Animator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registrations = models.ManyToManyField(Registration, blank=True)
    label = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    main_img = models.FileField(upload_to='animators', blank=True, null=True)
    animation_img = models.FileField(upload_to='animators', blank=True, null=True)
    general_order = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date_birth = models.DateField(blank=True, null=True)
    address = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    state = models.CharField(blank=True, null=True, max_length=100)
    consent_of_parent = models.BooleanField(default=False)
    consent_photo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Animator'

    def __str__(self):
        return f'animator: {self.user.last_name} {self.user.first_name}'


class Child(models.Model):
    class SwimStatus(models.TextChoices):
        NO = "NO", _("No")
        YES = "YES", _("Yes")
        ABIT = "ABIT", _("a little bit")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_number = models.CharField(blank=True, null=True, max_length=10, validators=[validate_rc])
    date_birth = models.DateField()
    address = models.CharField(blank=False, max_length=100)
    city = models.CharField(blank=False, max_length=100)
    state = models.CharField(blank=False, max_length=100)
    swim = models.CharField(max_length=4, choices=SwimStatus.choices, default=SwimStatus.NO)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Child'
        verbose_name_plural = 'Children'

    def __str__(self):
        return f'child: {self.user.last_name} {self.user.first_name}'


class ChildHealth(models.Model):
    disease_name = models.CharField(blank=False, max_length=100)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['disease_name', 'child']


class AnimatorHealth(models.Model):
    disease_name = models.CharField(blank=False, max_length=100)
    animator = models.ForeignKey(Animator, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['disease_name', 'animator']
        verbose_name = 'Animator disease'
        verbose_name_plural = 'Animator diseases'


class ChildParent(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['parent', 'child']


class Participant(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    advance_price = models.DecimalField(max_digits=20, decimal_places=2)
    paid = models.BooleanField(default=False)
    advance_paid = models.BooleanField(default=False)
    valid_participant = models.BooleanField(default=True)
    qr_diff = models.CharField(max_length=1000000, blank=True, null=True)
    qr_advance = models.CharField(max_length=1000000, blank=True, null=True)
    consent_agreement = models.BooleanField(default=False)
    consent_photo = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def generate_qr(self, due_date=datetime.now()):
        self.qr_advance = get_qr(
            iban=self.registration.bank_account,
            amount=self.advance_price,
            due_date=due_date,
            msg=f'{self.child.user.last_name} {self.child.user.first_name} zaloha {self.registration.label}'
        )
        self.qr_diff = get_qr(
            iban=self.registration.bank_account,
            amount=self.price - self.advance_price,
            due_date=self.registration.registration_end,
            msg=f'{self.child.user.last_name} {self.child.user.first_name} doplatok {self.registration.label}'
        )
        self.save()

    def confirm_mail(self, domain, parent=None):
        try:
            subject = f"Potvrdenie o registrácii na {self.registration.label}"
            email_template_name = "accounts/register_mail.txt"
            if not parent:
                parent = self.child.childparent_set.all()[0].parent
            c = {
                "child_name": f"{self.child.user.first_name} {self.child.user.last_name}",
                "user_name": parent.user.username,
                'profile_page': f'{domain}{reverse_lazy("profile")}',
                'reset_pwd_link': f'{domain}{reverse_lazy("password_reset")}',
            }
            email = render_to_string(email_template_name, c)
            if settings.EMAIL_ENABLED:
                send_mail(subject, email, settings.EMAIL_HOST_USER, [parent.contact_email], fail_silently=False)
        except Exception:
            logger.exception('Sending mail failed')

    class Meta:
        verbose_name = 'Participation'
        verbose_name_plural = 'Participation'


class ChildGroup(models.Model):
    label = models.CharField(max_length=100)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


class GroupAnimator(models.Model):
    animator = models.ForeignKey(Animator, on_delete=models.CASCADE)
    group = models.ForeignKey(ChildGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.label} {self.animator.label}"


class GroupChild(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    group = models.ForeignKey(ChildGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.label} - {self.child.user.last_name} {self.child.user.first_name}"

    class Meta:
        verbose_name_plural = 'Group Children'
