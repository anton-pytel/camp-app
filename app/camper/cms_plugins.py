from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from .models import Animator
from django.conf import settings

@plugin_pool.register_plugin
class AnimatorPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "tabor/animator.html"
    cache = False

    def render(self, context, instance, placeholder):
        animators = Animator.objects.filter(registrations__label=settings.VALID_REGISTRATION).order_by('general_order')
        context.update({'animators': animators})
        return context
