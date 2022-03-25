from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from .models import Animator

@plugin_pool.register_plugin
class AnimatorPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "tabor/animator.html"
    cache = False

    def render(self, context, instance, placeholder):
        animators = Animator.objects.filter()
        context.update({'animators': animators})
        return context