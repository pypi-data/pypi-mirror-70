from __future__ import absolute_import

from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils import compat, get_method_name
from stackifyapm.utils.helper import is_async_span


class Redis3CheckMixin(object):
    instrument_list_3 = []
    instrument_list = []

    def get_instrument_list(self):
        try:
            from redis import VERSION

            if VERSION[0] >= 3:
                return self.instrument_list_3
            return self.instrument_list
        except ImportError:
            return self.instrument_list


class RedisInstrumentation(Redis3CheckMixin, AbstractInstrumentedModule):
    name = "redis"

    instrument_list_3 = [("redis.client", "Redis.execute_command")]
    instrument_list = [("redis.client", "Redis.execute_command"), ("redis.client", "StrictRedis.execute_command")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        extra_data = {
            "wrapped_method": "execute",
            "provider": self.name,
            "type": "Cache",
            "sub_type": "cache",
            "operation": args and args[0] and args[0].lower() or get_method_name(method),
        }

        cache_name = len(args) > 1 and args[1] or None
        if isinstance(cache_name, compat.binary_type):
            extra_data['cache_key'] = cache_name.decode('utf-8')
        elif cache_name:
            extra_data['cache_key'] = str(cache_name)

        with CaptureSpan("cache.redis", extra_data, leaf=True, is_async=is_async_span()):
            return wrapped(*args, **kwargs)


class RedisPipelineInstrumentation(Redis3CheckMixin, AbstractInstrumentedModule):
    name = "redis"

    instrument_list_3 = [("redis.client", "Pipeline.execute")]
    instrument_list = [("redis.client", "BasePipeline.execute")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        operation = args and args[0] and args[0].lower() or get_method_name(method)
        cache_name = len(args) > 1 and args[1] or None

        if hasattr(instance, 'command_stack'):
            operation = instance.command_stack[0][0][0]
            cache_name = instance.command_stack[0][0][1]

        extra_data = {
            "wrapped_method": "execute",
            "provider": self.name,
            "type": "Cache",
            "sub_type": "cache",
            "operation": operation,
        }

        if isinstance(cache_name, compat.binary_type):
            extra_data['cache_key'] = cache_name.decode('utf-8')
        elif cache_name:
            extra_data['cache_key'] = str(cache_name)

        with CaptureSpan("cache.redis", extra_data, leaf=True, is_async=is_async_span()):
            return wrapped(*args, **kwargs)
