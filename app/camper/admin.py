from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from camper.models import *
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field


class ParticipantResource(resources.ModelResource):
    healtstat = Field(attribute='healtstat', column_name='healtstat')
    class Meta:
        model = Participant
        fields = [
            "id", "child__user__last_name", "child__user__first_name",
            "child__date_birth", "child__swim", "child__city", "consent_photo", "healtstat", "paid",
        ]
        export_order = (
            "id", "child__user__last_name", "child__user__first_name",
            "child__date_birth", "child__swim", "child__city", "consent_photo", "healtstat", "paid",
        )

    def dehydrate_healtstat(self, participation):
        res = []
        for dis in participation.child.childhealth_set.all():
            res.append(dis.disease_name)
        return ', '.join(res)


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


class ParentAdminInline(admin.StackedInline):
    model = Parent
    extra = 0
    inlines = [ChildParentAdminInline]


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


class ParentAdmin(admin.ModelAdmin):
    model = Parent
    list_display = ["user", "contact_phone", "contact_email", "updated"]


class ChildAdmin(admin.ModelAdmin):
    model = Child
    inlines = [ParticipantAdminInline, ChildParentAdminInline, ChildHealthInline]
    list_display = ["user", "date_birth", "swim", "city", "state"]


class ChildHealthAdmin(admin.ModelAdmin):
    model = ChildHealth
    list_display = ["disease_name", "child", "updated"]


class ParticipantAdmin(NestedModelAdmin, ImportExportModelAdmin):
    model = Participant
    resource_class = ParticipantResource
    list_display = ["registration", "child", "advance_price", "advance_paid", "price", "paid"]
    list_filter = ["registration", "paid"]


class AnimatorAdmin(NestedModelAdmin):
    model = Animator
    list_display = ["label", "general_order"]


class RegistrationAdmin(NestedModelAdmin):
    model = Registration
    list_display = ["label", "price", "advance_price", "registration_start", "registration_end" ]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Animator, AnimatorAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(ChildHealth, ChildHealthAdmin)
admin.site.register(ChildGroup, ChildGroupAdmin)

