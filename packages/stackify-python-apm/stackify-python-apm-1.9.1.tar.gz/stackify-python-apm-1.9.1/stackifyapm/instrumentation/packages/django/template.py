from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils import get_method_name


class DjangoTemplateInstrumentation(AbstractInstrumentedModule):
    name = "django_template"

    instrument_list = [("django.template", "Template.render")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        extra_data = {
            "wrapped_method": get_method_name(method),
            "provider": self.name,
            "type": "Template",
            "sub_type": "template",
        }

        if hasattr(instance, 'name'):
            extra_data['template'] = instance.name

        with CaptureSpan("template.django", extra_data):
            return wrapped(*args, **kwargs)


class DjangoTemplateSourceInstrumentation(AbstractInstrumentedModule):
    name = "django_template_source"
    instrument_list = [("django.template.base", "Parser.extend_nodelist")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        ret = wrapped(*args, **kwargs)

        if len(args) > 1:
            node = args[1]
        elif "node" in kwargs:
            node = kwargs["node"]
        else:
            return ret

        if len(args) > 2:
            token = args[2]
        elif "token" in kwargs:
            token = kwargs["token"]
        else:
            return ret

        if not hasattr(node, "token") and hasattr(token, "lineno"):
            node.token = token

        return ret
