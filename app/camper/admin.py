from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from camper.models import *


class ChildHealthInline(admin.StackedInline):
    model = ChildHealth
    extra = 0


class ParentInline(admin.StackedInline):
    model = Parent
    extra = 0


class Child4GroupInline(NestedTabularInline):
    model = Child
    extra = 0


class ParticipantAdmin(admin.StackedInline):
    model = Participant
    extra = 0


class ChildIAdmin(admin.ModelAdmin):
    model = Child
    extra = 0
    inlines = [ParticipantAdmin, ParentInline, ChildHealthInline]


class AnimatorInline(NestedTabularInline):
    model = Animator
    extra = 0


class GroupAnimatorInline(NestedTabularInline):
    model = GroupAnimator
    extra = 0
    inlines = [AnimatorInline]


class GroupChildInline(NestedTabularInline):
    model = GroupChild
    extra = 0
    inlines = [Child4GroupInline]


class ChildGroupAdmin(NestedModelAdmin):
    model = ChildGroup
    inlines = [GroupAnimatorInline, GroupChildInline]


admin.site.register(Registration)
admin.site.register(Parent)
admin.site.register(Animator)
admin.site.register(Child, ChildIAdmin)
admin.site.register(ChildGroup, ChildGroupAdmin)

