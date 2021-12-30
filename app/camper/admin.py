from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from camper.models import *
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


class ChildParentAdminInline(admin.StackedInline):
    model = ChildParent
    extra = 0


class ChildHealthInline(admin.StackedInline):
    model = ChildHealth
    extra = 0


class ChildInline(admin.StackedInline):
    model = Child
    extra = 0


class ParentInline(admin.StackedInline):
    model = Parent
    extra = 0


class Child4GroupInline(NestedTabularInline):
    model = Child
    extra = 0


class ParticipantAdminInline(admin.StackedInline):
    model = Participant
    extra = 0


class ParentAdmin(admin.StackedInline):
    model = Participant
    extra = 0
    inlines = [ChildParentAdminInline]


class ChildAdmin(admin.ModelAdmin):
    model = Child
    extra = 0
    inlines = [ParticipantAdminInline, ChildParentAdminInline, ChildHealthInline]


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


class ParticipantAdmin(NestedModelAdmin):
    model = Participant
    list_display = ["registration", "child", "price", "paid"]
    list_filter = ["registration", "paid"]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Registration)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Parent)
admin.site.register(Animator)
admin.site.register(Child, ChildAdmin)
admin.site.register(ChildGroup, ChildGroupAdmin)

