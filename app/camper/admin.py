from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from camper.models import *
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field


class ParticipantResource(resources.ModelResource):
    health_stat = Field(attribute='health_stat', column_name='health_stat')
    parents = Field(attribute='parents', column_name='parents')

    class Meta:
        model = Participant
        fields = [
            "id", "child__user__last_name", "child__user__first_name",
            "child__date_birth", "child__swim", "child__city", "consent_photo", "parents", "health_stat", "paid",
        ]
        export_order = (
            "id", "child__user__last_name", "child__user__first_name",
            "child__date_birth", "child__swim", "child__city", "consent_photo", "parents", "health_stat", "paid",
        )

    def dehydrate_health_stat(self, participation):
        res = []
        for dis in participation.child.childhealth_set.all():
            res.append(dis.disease_name)
        return ', '.join(res)

    def dehydrate_parents(self, participation):
        res = []
        for parent_item in participation.child.childparent_set.all():
            res.append(f"{parent_item.parent.user.last_name} {parent_item.parent.user.last_name} - "
                       f"{parent_item.parent.contact_phone} - {parent_item.parent.contact_email}")
        return '\n'.join(res)


class AnimatorResource(resources.ModelResource):
    health_stat = Field(attribute='health_stat', column_name='health_stat')

    class Meta:
        model = Animator
        fields = [
            "user__id", "user__last_name", "user__first_name",
            "date_birth", "address", "city", "state",
            "consent_of_parent", "consent_photo", "health_stat",
        ]
        export_order = (
            "user__id", "user__last_name", "user__first_name",
            "date_birth", "address", "city", "state",
            "consent_of_parent", "consent_photo", "health_stat",
        )

    def dehydrate_health_stat(self, animator):
        res = []
        for dis in animator.animatorhealth_set.all():
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


class AnimatorHealthInline(admin.StackedInline):
    model = AnimatorHealth
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


class GroupAnimatorInline(admin.TabularInline):
    model = GroupAnimator
    extra = 0
    # inlines = [AnimatorInline]


class GroupChildInline(admin.TabularInline):
    model = GroupChild
    extra = 0
    # inlines = [Child4GroupInline]


class ChildGroupAdmin(admin.ModelAdmin):
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
    list_display = [
        "registration", "advance_price", "advance_paid", "price", "paid", "get_date_birth",
        "get_last_name", "get_first_name", "get_address", "get_city", "get_swim"
    ]
    list_filter = [
        "registration", "paid", "child__user__first_name", "child__user__last_name",
        "child__date_birth", "child__swim", "child__address",
        "child__city"
    ]

    def get_first_name(self, obj):
        return obj.child.user.first_name

    get_first_name.admin_order_field = 'child__user__first_name'  # Allows column order sorting
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.child.user.last_name

    get_last_name.admin_order_field = 'child__user__last_name'  # Allows column order sorting
    get_last_name.short_description = 'Last Name'

    def get_address(self, obj):
        return obj.child.address

    get_address.admin_order_field = 'child__address'  # Allows column order sorting
    get_address.short_description = 'Address'

    def get_city(self, obj):
        return obj.child.city

    get_city.admin_order_field = 'child__city'  # Allows column order sorting
    get_city.short_description = 'City'

    def get_date_birth(self, obj):
        return obj.child.date_birth

    get_date_birth.admin_order_field = 'child__date_birth'  # Allows column order sorting
    get_date_birth.short_description = 'Date birth'

    def get_swim(self, obj):
        return obj.child.swim

    get_swim.admin_order_field = 'child__swim'  # Allows column order sorting
    get_swim.short_description = 'Swim'



class AnimatorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Animator
    resource_class = AnimatorResource
    list_display = ["label", "get_username", "general_order", "consent_of_parent", "consent_photo"]
    list_filter = ["registrations"]
    inlines = [AnimatorHealthInline]

    def get_username(self, animator):
        return animator.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'


class RegistrationAdmin(admin.ModelAdmin):
    model = Registration
    list_display = ["label", "price", "advance_price", "registration_start", "registration_end"]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Animator, AnimatorAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(ChildHealth, ChildHealthAdmin)
admin.site.register(ChildGroup, ChildGroupAdmin)

