"""
    Dependency injection with decorator
"""

from functools import wraps
import inspect


# TODO This context registry won't work in real scenarios
# TODO where this module will be imported just once.
_named_contexts = {}


def set_named_context(name, context):
    _named_contexts[name] = context


def get_named_context(name):
    return _named_contexts[name] if name in _named_contexts else {}


def inject(f=None, **options):

    context_option = options.get('context')

    def decorator(f):

        # Inspect only when the function is first decorated
        f._arg_names = inspect.getargspec(f).args

        @wraps(f)
        def wrapped_func(*args, **kwargs):

            # Context is resolved only on method invocation
            if isinstance(context_option, basestring):
                context = get_named_context(context_option)
            elif isinstance(context_option, dict):
                context = context_option
            else:
                context = {}

            for name in f._arg_names:
                if name in context:
                    kwargs[name] = context[name]

            return f(*args, **kwargs)

        return wrapped_func

    if f:
        return decorator(f)
    else:
        return decorator


class Adapter(object):

    def get_content(self):
        return 'Here is some content from Adapter'


@inject(context='my_context')
def greeting(subject=None):
    return 'Hello {}!'.format(subject)


@inject(context='my_context')
def get_content(adapter=None):
    return adapter.get_content()

set_named_context('my_context', {
    'subject': 'Linda',
    'adapter': Adapter()
})

print greeting()
print get_content()

set_named_context('my_context', {
    'subject': 'Harry',
    'adapter': Adapter()
})

print greeting()
print get_content()
