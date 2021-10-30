from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Registration(models.Model):
    label = models.CharField(default="tabor2022", max_length=100)
    registration_start = models.DateField()
    registration_end = models.DateField()
    camp_start_date = models.DateField()
    camp_start_end = models.DateField()


class Parent(User):
    consent = models.BooleanField(default=False)


class Animator(User):
    pass


class Child(User):
    class SwimStatus(models.TextChoices):
        NO = "NO", _("No")
        YES = "YES", _("Yes")
        ABIT = "ABIT", _("a little bit")

    rc = models.CharField(blank=False, unique=True, max_length=10)
    address = models.CharField(blank=False, unique=True, max_length=100)
    city = models.CharField(blank=False, unique=True, max_length=100)
    state = models.CharField(blank=False, unique=True, max_length=100)
    swim = models.CharField(max_length=4, choices=SwimStatus.choices, default=SwimStatus.NO)


class ChildHealth(models.Model):
    name = models.CharField(default="name", blank=False, unique=True, max_length=100)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)


class ChildParent(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)


class Participant(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    paid = models.BooleanField(default=False)


class ChildGroup(models.Model):
    label = models.CharField(max_length=100)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)


class GroupAnimator(models.Model):
    animator = models.ForeignKey(Animator, on_delete=models.CASCADE)
    group = models.ForeignKey(ChildGroup, on_delete=models.CASCADE)


class GroupChildren(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    group = models.ForeignKey(ChildGroup, on_delete=models.CASCADE)

